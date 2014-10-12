"""
@author: Julien Zoubian
@organization: CPPM
@copyright: Gnu Public Licence
@contact: zoubian@cppm.in2p3.fr

TIPS classes to manage observation objects.
"""
import os
import pyfits
import tips

from tipserror import *
from tipsinstrument import *
from tipssky import *

tipsDataDir = tips.__path__[0]+'/data/'

## define simulation function separatly to able parallel computing with pp
#def pp_run_single(workDir, dataDir, spectro, skySrc, skyBck, exptime, debug, norm):
#       simulation = tips.tipsaxesim.Simulation(workDir, dataDir)
#       simulation.prepInstrument(spectro)
#       simulation.prepSky(skySrc, spectro, skyBck)
#       
#       # close model spectra to avoid memory leak
#       skySrc.closeSpc()
#
#       simulation.run(exptime, spectro, debug, norm)
#
#       simulation.close()

class Observation:
        """
        Class to simulate observation
        """
        
        def __init__(self, inCatDir=None, inSpcDir=None, inCatForm='TIPS', inSpcForm='TIPS', debug=False, norm=False, silent=True, inThmDir=None, inThmForm='TIPS'):
                """
                Constructor: initialize the class

                """
                
                # init sky model
                self.skySrc = SkySources(inCatDir, inSpcDir, inCatForm, inSpcForm, inThmDir, inThmForm, silent)
                
                # init instrument model
                self.instrument = None
                
                self.debug = debug
                self.norm = norm
                self.silent = silent
                
                self.dataDir = None
                self.confDir = None
                
                self.nexpo = 0

        def loadEUCLIDDefault(self, grismName='Gblue0', exptime=560.0, ra0=0.0, dec0 = 0.0, orient=0.0, x0=0.0, y0=0.0):
                """
                Method to load default EUCLID/NISP observation
                
                param exptime: exposure time
                type exptime: float
                param ra0: right ascension of down left corner of the field of view
                type ra0: float
                param dec0: declinaison of down left corner of the field of view
                type dec0: float
                """
                
                # load EUCLID configuration
                if self.instrument != None:
                        self.instrument.close()
                self.instrument = FocalPlan()
                self.instrument.loadEUCLIDDefault(ra0=ra0, dec0=dec0, orient=orient, grism=grismName, exptime=exptime, x0=x0, y0=y0)
                
                # set the sky background to a constante value in photon/s/pix in the detector plan
                # this value include sky backgroud, scattering and thermal noise
                if grismName=='Gblue0' or grismName=='Gblue90':
                  self.instrument.setSkyBck(0.66)
                elif grismName=='Gred0' or grismName=='Gred90':
                  self.instrument.setSkyBck(0.53)
                
                self.dataDir = tipsDataDir
                self.confDir = None

        def loadFromFile(self, fileName, exptime=None, ra0=None, dec0 = None, orient=None, x0=None, y0=None):
                """
                Method to load observation model from a file.
                """

                self.dataDir = None
                self.confDir = fileName
                
                conf = pyfits.open(fileName)
                
                # first load the observation parameters

                if ra0 == None:
                  ra0 = float(conf[0].header['RA0'])
                if dec0 == None:
                  dec0 = float(conf[0].header['DEC0'])
                if orient == None:
                  try:
                    orient = float(conf[0].header['ORIENTAT'])
                  except (KeyError, ValueError):
                    orient = 0.0
                if x0 == None:
                  try:
                    x0 = float(conf[0].header['X0'])
                  except (KeyError, ValueError):
                    x0 = 0.0
                if y0 == None:
                  try:
                    y0 = float(conf[0].header['Y0'])
                  except (KeyError, ValueError):
                    y0 = 0.0

                # set the instrument model
                if self.instrument != None:
                        self.instrument.close()
                        
                try:
                        self.nexpo = int(conf[0].header['NEXPO'])
                except (KeyError, ValueError):
                        self.nexpo = 0
                        
                self.instrument = FocalPlan()
                if self.nexpo == 0:
                       self.instrument.loadFromConf(conf, hconf=0, ra0=ra0, dec0=dec0, exptime=exptime, orient=orient, x0=x0, y0=y0)
                else:
                    for h in range(self.nexpo):
                        hconf = str(conf[0].header['EXPO'+str(h)])
                        try:
                            ditra = float(conf[hconf].header['DITRA'])
                        except (KeyError, ValueError):
                            ditra = 0.0
                        try:
                            ditdec = float(conf[hconf].header['DITDEC'])
                        except (KeyError, ValueError):
                            ditdec = 0.0
                        ra0 += ditra
                        dec0 += ditdec
                        self.instrument.loadFromConf(conf, hconf=hconf, ra0=ra0, dec0=dec0, exptime=exptime, orient=orient, x0=x0, y0=y0)
                    
                conf.close()
                del conf
                
        def getSpectros(self, expname=None):
                """
                Method to get the list of spectro images to simulate
                """
                
                if expname==None:
                    return self.instrument.spectros
                else:
                    rList = []
                    for i in range(len(self.instrument.spectros)):
                        if self.instrument.spectros[i].expname == expname:
                            rList.append(self.instrument.spectros[i])
                    if len(rList)==0:
                        error_message = 'No exposure named %s was found' % expname
                        raise TIPSError(error_message)
                    else:
                        return rList
                 
        def runOneSim(self, spectro, workDir='./'):
                """
                Method to run a single detector simulation
                """
                simulation = tips.tipsaxesim.Simulation(workDir, self.dataDir, self.confDir, debug=self.debug, silent=self.silent)
                simulation.prepInstrument(spectro)
                simulation.prepSky(self.skySrc, spectro)
                # close model spectra to avoid memory leak
                self.skySrc.closeSpc()

                simulation.run(spectro, norm=self.norm)

                simulation.close()      

        def runSimulation(self, workDir='./', ncpu = 0):
                if ncpu>1:
                        warning_message = "Because of some troubles with pp module, parallel coputation is disable for now. Computation will be run on one cpu."
                        print warning_message
                        #try:
                        #       import pp
                        #       ppservers=("*",)
                        #       job_server = pp.Server(ncpu, ppservers=ppservers, secret='TIPS')
                        #       jobs=[]
                        #       # init directory before to avoid some bug
                        #       simulation = tips.tipsaxesim.Simulation(workDir, self.dataDir)
                        #       simulation.close()
                        #       del simulation
                        #       for spectro in self.instrument.spectros:
                        #               jobs.append(job_server.submit(pp_run_single, (workDir, self.dataDir, spectro, self.skySrc, self.skyBck, self.exptime, self.debug, self.norm), (), ('numpy', 'scipy', 'tips', 'axesim')))
                        #       #for job in jobs:
                        #       #       print job()
                        #       # wait all job finish to avoid some bug
                        #       job_server.wait()
                        #except ImportError:
                        #       error_message = 'ImportError: No module named pp.'
                        #       raise TIPSError(error_message)
                #else:
                
                for spectro in self.instrument.spectros:
                        self.runOneSim(spectro, workDir)

        def close(self):

                if self.instrument != None:
                        self.instrument.close()
                else:
                        del self.instrument

                if self.skySrc != None:
                        self.skySrc.close()
                else:
                        del self.skySrc

                del self
