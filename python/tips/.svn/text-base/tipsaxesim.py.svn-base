"""
@author: Julien Zoubian
@organization: CPPM
@copyright: Gnu Public Licence
@contact: zoubian@cppm.in2p3.fr

TIPS classes to manage aXeSIM.
"""

import os
import shutil
import sys
import asciidata
import pyfits
import numpy
import copy

from axesim import *
from tipserror import *
from tipsinstrument import *
from tipssky import *

def mkdir(dir):
  # function to make directory
  if os.path.exists(dir):
    if not os.path.isdir(dir):
      print """
Error: %s alredy exist and is not a directory!
      """
      sys.exit()
  else:
      os.mkdir(dir)

class Simulation:
        """
        Class to simulate grism image with aXeSIM
        """
        
        def __init__(self, workDir, dataDir, confDir, silent=True, debug=False):
                """
                Constructor: init the class
                
                param workDir: path where axesim will be run
                type workDir: string
                param dataDir: path to refenrence file directory
                type workDir: string
                """
                
                self.workDir = workDir
                self.dataDir = dataDir
                self.confDir = confDir
                
                # set the aXe working path
                mkdir(self.workDir)
                mkdir(self.workDir+'/DATA')
                mkdir(self.workDir+'/CONF')
                mkdir(self.workDir+'/OUTPUT')
                mkdir(self.workDir+'/OUTSIM')
                mkdir(self.workDir+'/SIMDATA')
                mkdir(self.workDir+'/DRIZZLE')
                
                self.bck = None
                self.motName = None
                self.modSpecName = None
                self.modImgName = None
                self.confName = None
                self.outImgName = None
                self.ngal = 0
                
                self.silent = silent
                self.debug = False
                
        def prepInstrument(self, spectroModel, confName = None):
                """
                Method to prepare aXeSIM configuration files
                
                param spectroModel: spectro model
                type spectroModel: Spectrometer
                """
                
                if confName == None:
                        end = spectroModel.version+spectroModel.model+spectroModel.date+'.conf'
                        self.confName = spectroModel.idientier+'_'+spectroModel.grism.idientier+'_'+str(spectroModel.detector.idientier)+end
                else:
                        self.confName = confName
                        
                # copy sensibility files
                if self.confDir != None:
                        conf = pyfits.open(self.confDir)
                for b in spectroModel.grism.beams:
                        if self.confDir != None:
                                sensout = self.workDir+'/CONF/'+b.get_sens_output()
                                if not os.path.exists(sensout):
                                        sens = pyfits.HDUList(pyfits.PrimaryHDU())
                                        sens.append(conf[b.sensitivity])
                                        sens.writeto(sensout)
                                        sens.close()
                        else:
                                sensname = b.get_sens_output()
                                ext = sensname.split('.')[-1]
                                b.sensitivity = self.confName+'_'+b.idientier+'.'+ext
                                shutil.copy(self.dataDir+'/'+sensname, self.workDir+'/CONF/'+b.sensitivity)
                        
                # copy detector maps
                if self.confDir != None:
                        if  spectroModel.detector.get_map_output('RN') != 'None':
                                try:
                                        f = float(spectroModel.detector.rn)
                                except (TypeError, ValueError):
                                        mapdir = self.workDir+'/CONF/'+spectroModel.detector.get_map_output('RN')
                                        if not os.path.exists(mapdir):
                                                mapfile = pyfits.HDUList(pyfits.PrimaryHDU())
                                                mapfile.append(conf[spectroModel.detector.rn])
                                                mapfile.writeto(mapdir)
                                                mapfile.close()
                        if  spectroModel.detector.get_map_output('DC') != 'None':
                                try:
                                        f = float(spectroModel.detector.dc)
                                except (TypeError, ValueError):
                                        mapdir = self.workDir+'/CONF/'+spectroModel.detector.get_map_output('DC')
                                        if not os.path.exists(mapdir):
                                                mapfile = pyfits.HDUList(pyfits.PrimaryHDU())
                                                mapfile.append(conf[spectroModel.detector.dc])
                                                mapfile.writeto(mapdir)
                                                mapfile.close()
                        if  spectroModel.detector.get_map_output('QE') != 'None':
                                try:
                                        f = float(spectroModel.detector.qe)
                                except (TypeError, ValueError):
                                        mapdir = self.workDir+'/CONF/'+spectroModel.detector.get_map_output('QE')
                                        if not os.path.exists(mapdir):
                                                mapfile = pyfits.HDUList(pyfits.PrimaryHDU())
                                                mapfile.append(conf[spectroModel.detector.qe])
                                                mapfile.writeto(mapdir)
                                                mapfile.close()
                        if  spectroModel.detector.get_map_output('COS') != 'None':
                                try:
                                        f = float(spectroModel.detector.cmap)
                                except (TypeError, ValueError):
                                        mapdir = self.workDir+'/CONF/'+spectroModel.detector.get_map_output('COS')
                                        if not os.path.exists(mapdir):
                                                mapfile = pyfits.HDUList(pyfits.PrimaryHDU())
                                                mapfile.append(conf[spectroModel.detector.cmap])
                                                mapfile.writeto(mapdir)
                                                mapfile.close()
                                
                if self.confDir != None:
                        conf.close()

                # write configuration file in CONF directory
                spectroModel.writeaXeConf(self.workDir+'/CONF/'+self.confName)
                
        def importBck(self, skyBck):
                """
                Method to set sky background for aXeSIM
                """
                if skyBck!=None:
                        try:
                            # to convert the background value
                            # to a float
                            self.bck = float(skyBck)
                        except (TypeError, ValueError):
                                if self.confDir != None:
                                        self.bck = skyBck+'.fits'
                                        mapdir = self.workDir+'/CONF/'+self.bck
                                        if os.path.exists(mapdir):
                                                warning_message = 'Warning: the file %s already exist and have not be overwrited.' % mapdir
                                                print TIPSWarning(warning_message)
                                        else:
                                                conf = pyfits.open(self.confDir)
                                                mapfile = pyfits.HDUList(pyfits.PrimaryHDU())
                                                mapfile.append(conf[skyBck])
                                                mapfile.writeto(mapdir)
                                                mapfile.close()
                                                conf.close()
                                else:
                                        error_message = 'Error: Only constante sky background is implemented for now.'
                                        raise TIPSError(error_message)
        
        def importSrc(self, skySrc, spectroModel):
                """
                Method to set the Model Object Table for aXeSIM
                """
                
                if spectroModel.skyAbs!=None:
                        error_message = 'Error: sky absorption is not implemented for now'
                        raise TIPSError(error_message)
                
                # get cat name
                catname = skySrc.inCatDir.split("/")[-1]
                # remove extention
                catroot = '.'.join(catname.split(".")[:-1])
                # set MOT name

                self.motName = catroot+'_'+spectroModel.idientier+'_'+spectroModel.grism.idientier+'_'+str(spectroModel.detector.idientier)+'.cat'
                self.modSpecName = self.motName.replace('.cat','.spc.fits')
                
                if skySrc.inThmDir != None or skySrc.inThmForm=='Split':
                    self.modImgName = self.motName.replace('.cat','.thm.fits')
                
                # set box limit (not optimal, could be smaller in taking into account the spectra angle)
                b = spectroModel.grism.beams[0]
                d = spectroModel.detector
                xmin = -b.xoff-b.xend
                xmax = d.nx-b.xstart-b.xoff
                ymin = -b.yoff-b.xend
                ymax = d.ny-b.xstart-b.yoff
                if len(spectroModel.grism.beams)>1:
                  for b in spectroModel.grism.beams[1:]:
                    if xmin>(-b.xoff-b.xend):
                      xmin = -b.xoff-b.xend
                    if xmax<(d.nx-b.xstart-b.xoff):
                      xmax = d.nx-b.xstart-b.xoff
                    if ymin>(-b.yoff-b.xend):
                      ymin = -b.yoff-b.xend
                    if ymax<(d.ny-b.xstart-b.yoff):
                      ymax = d.ny-b.xstart-b.yoff
                      
                # get wcs data
                wcs = copy.copy(spectroModel.wcs)
                if spectroModel.rot90:
                    wcs.rotateCD(90.0, centered=True)
                    if spectroModel.dlim != None and spectroModel.dlim > xmin:
                        xmin = spectroModel.dlim
                    if spectroModel.ulim != None and spectroModel.ulim < xmax:
                        xmax = spectroModel.ulim    
                else:
                    if spectroModel.llim != None and spectroModel.llim > xmin:
                        xmin = spectroModel.llim
                    if spectroModel.rlim != None and spectroModel.rlim < xmax:
                        xmax = spectroModel.rlim    
                
                # make aXeSIM MOT
                ra = skySrc.getCatCol('RA')
                dec = skySrc.getCatCol('DEC')
                
                (x_img, y_img) = wcs.rd2xy(ra, dec)

                # Note: A_IMAGE and B_IMAGE (approximation, no sky curve)
                a_img = skySrc.getCatCol('A_SKY')/d.scale
                b_img = skySrc.getCatCol('B_SKY')/d.scale
                t_img = skySrc.getCatCol('THETA_SKY')+wcs.orient
                
                ids = skySrc.getCatCol('NUMBER')
                
                # select sources in the detector field
                xysel = (x_img>=xmin)&(x_img<=xmax)&(y_img>=ymin)&(y_img<=ymax)
                ids = ids[xysel]
                self.ngal = len(ids)
                if self.ngal > 0:
                        #print "Prepare aXeSIM input sources: %d" % len(ids)
                        x_img = x_img[xysel]
                        y_img = y_img[xysel]
                        a_img = a_img[xysel]
                        b_img = b_img[xysel]
                        t_img = t_img[xysel]
                        
                        # make a dummy mag col (useless but needed by axesim)
                        mag = numpy.ones(len(ids))*22.0
                        
                        # write MOT to axesim path
                        outcat = asciidata.createSEx(10,len(ids))
                        outcat[0].rename('NUMBER')
                        outcat[1].rename('X_IMAGE')
                        outcat[2].rename('Y_IMAGE')
                        outcat[3].rename('A_IMAGE')
                        outcat[4].rename('B_IMAGE')
                        outcat[5].rename('THETA_IMAGE')
                        outcat[6].rename('MODSPEC')
                        outcat[7].rename('MODIMAGE')
                        outcat[8].rename('MAG_J1220')
                        outcat[9].rename('ID')
                        outspc = pyfits.HDUList(pyfits.PrimaryHDU())
                        if self.modImgName != None:
                            outthm = pyfits.HDUList(pyfits.PrimaryHDU())
                        
                        for i in range(len(ids)):
                                #sys.stdout.write('%i / %i \r' % (i+1,len(ids)))
                                #sys.stdout.flush()
                                outcat['NUMBER'][i] = i+1
                                outcat['ID'][i] = ids[i]
                                outcat['X_IMAGE'][i] = x_img[i]
                                outcat['Y_IMAGE'][i] = y_img[i]
                                outcat['A_IMAGE'][i] = a_img[i]
                                outcat['B_IMAGE'][i] = b_img[i]
                                outcat['THETA_IMAGE'][i] = t_img[i]
                                outcat['MODSPEC'][i] = i+1
                                outcat['MODIMAGE'][i] = 0
                                outcat['MAG_J1220'][i] = mag[i]
                                
                                (wave,flux) = skySrc.getSpcIdent(ids[i])
                                c1=pyfits.Column(name='WAV_NM', format='E', array=(wave/10.))
                                c2=pyfits.Column(name='FLUX', format='E', array=(flux))
                                outspc.append(pyfits.new_table([c1,c2]))
                                outspc[-1].header.update('ID', ids[i])
                                outspc[-1].header.update('NUMBER', i+1)
                                
                                if self.modImgName != None:
                                    (modimg, smpfac) = skySrc.getThmIdent(ids[i], pixscl=d.scale)
                                    outcat['MODIMAGE'][i] = i+1
                                    outthm.append(pyfits.ImageHDU(modimg))
                                    outthm[-1].header.update('ID', ids[i])
                                    outthm[-1].header.update('NUMBER', i+1)
                                    if smpfac != None:
                                        outthm[-1].header.update('SMPFAC', smpfac)
                                    
                        #print '%i / %i \r' % (i+1,len(ids))
                        
                        outcat.writeto(self.workDir+'/DATA/'+self.motName)
                        del outcat
                        if os.path.exists(self.workDir+'/DATA/'+self.modSpecName):
                                os.unlink(self.workDir+'/DATA/'+self.modSpecName)
                        outspc.writeto(self.workDir+'/DATA/'+self.modSpecName)
                        outspc.close()
                        del outspc
                        if self.modImgName != None:
                            if os.path.exists(self.workDir+'/DATA/'+self.modImgName):
                                os.unlink(self.workDir+'/DATA/'+self.modImgName)
                            outthm.writeto(self.workDir+'/DATA/'+self.modImgName)
                            outthm.close()
                            del outthm
                        del mag

                else:
                        if not self.silent:
                            warning_message = 'Number of sources is %d !' % self.ngal
                            print TIPSWarning(warning_message)
                
                del ra
                del dec
                del x_img
                del y_img
                del a_img
                del b_img
                del t_img
                del ids
                del xysel

        def prepSky(self, skySrc, spectroModel):
                """
                Method to prepare aXeSIM sky inputs
                """

                self.importBck(spectroModel.skyBck)
                if skySrc.inCat != None:
                    self.importSrc(skySrc, spectroModel)
        
        def run(self, spectroModel, outImgName=None, norm=False):
                """
                Method to run aXeSIM sky inputs
                """
                
                # set out image name
                if outImgName == None:
                        end = spectroModel.version+spectroModel.model+spectroModel.date+'_IMG.fits'
                        if self.motName != None:
                            self.outImgName = self.motName.replace('.cat',end)
                        else:
                            self.outImgName = "dark_"+spectroModel.idientier+'_'+spectroModel.grism.idientier+'_'+str(spectroModel.detector.idientier)+end
                else:
                        self.outImgName = outImgName
                
                # set environnement variable (needed by aXeSIM)
                os.environ['AXE_IMAGE_PATH'] = self.workDir+'/DATA/'
                os.environ['AXE_CONFIG_PATH']  = self.workDir+'/CONF/'
                os.environ['AXE_OUTPUT_PATH']  = self.workDir+'/OUTPUT/'
                os.environ['AXE_OUTSIM_PATH']  = self.workDir+'/OUTSIM/'
                os.environ['AXE_SIMDATA_PATH'] = self.workDir+'/SIMDATA/'
                os.environ['AXE_DRIZZLE_PATH'] = self.workDir+'/DRIZZLE/'
                
                if self.ngal==0:
                    if not self.silent:
                        warning_message = 'No source in the simulated field : '+spectroModel.idientier+'_'+spectroModel.grism.idientier+'_'+str(spectroModel.detector.idientier)+end
                        print TIPSWarning(warning_message)
                    self.motName = None
                    self.modSpecName = None
                    self.modImgName = None

                # run the simulation
                simdispim(incat=self.motName, config=self.confName, dispim_name=self.outImgName,
                          model_spectra=self.modSpecName, bck_flux=self.bck, exptime=spectroModel.exptime,
                          model_images=self.modImgName, debug=self.debug, norm=norm, silent=self.silent)

                img = pyfits.open(self.workDir+'/OUTSIM/'+self.outImgName, mode='update')
                # rotate image if needed
                if spectroModel.rot90:
                    if self.debug:
                        shutil.copy(self.workDir+'/OUTSIM/'+self.outImgName, self.workDir+'/OUTSIM/'+self.outImgName.replace('.fits', '_norot.fits'))
                    sci = img['SCI'].data
                    err = img['ERR'].data
                    dq = img['DQ'].data
                    img['SCI'].data = numpy.copy(numpy.rot90(sci))
                    img['ERR'].data = numpy.copy(numpy.rot90(err))
                    img['DQ'].data = numpy.copy(numpy.rot90(dq))
                # set the headers
                for ext in ['SCI','ERR','DQ']:
                    img[ext].header.update('WCSAXES', 2)
                    img[ext].header.update('CRPIX1', spectroModel.wcs.crpix1)
                    img[ext].header.update('CRPIX2', spectroModel.wcs.crpix2)
                    img[ext].header.update('CRVAL1', spectroModel.wcs.crval1)
                    img[ext].header.update('CRVAL2', spectroModel.wcs.crval2)
                    img[ext].header.update('CTYPE1', 'RA---TAN')
                    img[ext].header.update('CTYPE2', 'DEC--TAN')
                    img[ext].header.update('CD1_1', spectroModel.wcs.cd11)
                    img[ext].header.update('CD1_2', spectroModel.wcs.cd12)
                    img[ext].header.update('CD2_1', spectroModel.wcs.cd21)
                    img[ext].header.update('CD2_2', spectroModel.wcs.cd22)
                    img[ext].header.update('ORIENTAT', spectroModel.wcs.orient)
                    img[ext].header.update('LTV1', 0.0)
                    img[ext].header.update('LTV2', 0.0)
                    img[ext].header.update('LTM1_1', 1.0)
                    img[ext].header.update('LTM2_2', 1.0)
                    img[ext].header.update('RA_APER', spectroModel.wcs.crval1)
                    img[ext].header.update('DEC_APER', spectroModel.wcs.crval2)
                    img[ext].header.update('PA_APER', spectroModel.wcs.orient)
                    img[ext].header.update('VAFACTOR', 1.0)
                    img[ext].header.update('EXPNAME', spectroModel.version+spectroModel.model+spectroModel.date)
                
                img.flush()
                img.close()
                                    
                del img
                if spectroModel.rot90:
                    del sci
                    del err
                    del dq

        def close(self):
                del self.workDir
                del self.dataDir                
                del self.bck
                del self.motName
                del self.modSpecName
                del self.modImgName
                del self.confName
                del self.outImgName
                del self.ngal
                del self
                
