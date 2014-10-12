"""
@author: Julien Zoubian
@organization: CPPM
@copyright: Gnu Public Licence
@contact: zoubian@cppm.in2p3.fr

TIPS classes to manage instrument objects.
"""
import pyfits
import copy
import numpy

from tipserror import *

class Detector:
  """
  Class to model a detector
  """
  
  def __init__(self):
    """
    Constructor: Initialize the class
    """
    
    # detector parameters
    self.rn = 0.0
    self.qe = 0.0
    self.dc = 0.0
    self.nx = 0
    self.ny = 0
    self.nbit = 0
    
    self.scale = 0.0
    self.size = 0.0
    
    # calibration files
    self.ffname = None
    self.expname = None
    
    # comics
    self.cmap = None
    self.reject = None

    self.idientier = None
    self.mapext = ''
    
    self.rdmode = 'Default'
    
    self.vrn = ''
    self.vqe = ''
    self.vdc = ''
    self.vcmap = ''
    self.drn = ''
    self.dqe = ''
    self.ddc = ''
    self.dcmap = ''   
    
  def loadEUCLIDdefault(self, id=1):
    """
    Method to load default EUCLID configuration
    """
    
    self.idientier = id
    self.mapext = ''
    
    self.rn = 6.0
    self.qe = 0.75
    self.dc = 0.1
    self.nx = 2040
    self.ny = 2040
    self.nbit = 16
    
    self.scale = 0.3
    self.size = 18.0

  def get_map_value(self, conf, keymap, hconf=0):
    # test to read specific keyword
    try:
      value = conf[hconf].header[keymap+str(self.idientier)]
    except KeyError:
      value = conf[hconf].header[keymap]
    # test if it is a map or a float
    try:
      return (float(value), '', '')
    except ValueError:
        try:
            version = '_v'+str(conf[value].header['VERSION'])
        except (KeyError, ValueError):
            version = ''
        try:
            date = '_d'+str(conf[value].header['DATE'])
        except (KeyError, ValueError):
            date = ''
        self.sensext = '.fits'
        return (value, version, date)

  def get_map_output(self, name):
    if name=='RN':
        value=self.rn
        version = self.vrn
        date = self.drn
    elif name=='QE':
        value=self.qe
        version = self.vqe
        date = self.dqe
    elif name=='DC':
        value=self.dc
        version = self.vdc
        date = self.ddc
    elif name=='COS':
        value=self.cmap
        version = self.vcmap
        date = self.dcmap
    else:
        return 'None'
    
    try:
      f = float(value)
      return str(value)
    except (TypeError, ValueError):
      if value == None or value == 'None':
        return 'None'
      else:
        return value + version + date + self.mapext

  def loadFromConf(self, conf, hconf=0, id=1):
    """
    Method to load a detector model
    """
    self.idientier = id
    self.mapext = '.fits'
    
    self.nx = int(conf[0].header['NPIXX'])
    self.ny = int(conf[0].header['NPIXY'])
    self.scale = float(conf[0].header['PIXSCALE'])
    self.size = float(conf[0].header['PIXSIZE'])

    (self.rn, self.vrn, self.drn) = self.get_map_value(conf, 'RN')
    (self.qe, self.vqe, self.dqe) = self.get_map_value(conf, 'QE')
    (self.dc, self.vdc, self.ddc) = self.get_map_value(conf, 'DC')
    try:
      (self.cmap, self.vcmap, self.dcmap) = self.get_map_value(conf, 'COSMAP', hconf)
    except KeyError:
      self.cmap = None
      self.vcmap = ''
      self.dcmap = ''
    try:
        self.nbit = int(conf[0].header['NBIT'])
    except ValueError:
        if conf[0].header['NBIT'] != 'None':
            raise "Error: NBIT = %s is not valid" % (conf[0].header['NBIT'])
        else:
            self.nbit = 'None'
    except KeyError:
        self.nbit = 16
    try:
        self.reject = conf[0].header['REJECT']
    except KeyError:
        self.reject = 'None'
    try:
        self.rdmode = conf[0].header['RDMODE']
    except KeyError:
        self.rdmode = 'Default'      
    
    #self.ngrp 
    #self. nfrm 
    #self.dtgrp 
    #self.dtfrm 
    
  def printParams(self):
    """
    Method to print detector configuration
    """
    
    print "# pixels properties"
    print "RDNOISE %s" % (str(self.rn))
    print "DC %s" % (str(self.dc))
    print "QE %s" % (str(self.qe))
    print "NPIXX %d" % (self.nx)
    print "NPIXY %d" % (self.ny)
    print "FFNAME %s" % (str(self.ffname))
    print "EXPNAME %s" % (str(self.expname))
    print "NBIT %s" % (str(self.nbit))
    print "COSMAP %s" % (str(self.cmap))
    print "REJECT %s" % (str(self.reject))
    print ""

  def close(self):
    del self.rn
    del self.qe
    del self.dc
    del self.nx 
    del self.ny 
    del self.scale
    del self.size 
    del self.ffname
    del self.expname   
    del self.idientier
    del self

class Beam:
  """
  Class to model a beam
  """
  
  def __init__(self):
    """
    Constructor: Initialize the class
    """
    
    self.idientier = None
        
    # trace description
    self.xstart = 0.0
    self.xend = 0.0
    self.odydx = 0
    self.dydx = []
    
    # x and y offsets
    self.xoff = 0.0
    self.yoff = 0.0

    self.sig1 = None
    self.sig2 = None
    self.c = None 
    
    # dispersion solution
    self.odldp = 0
    self.dldp = []
    
    # sensitivity
    self.sensitivity = None
    self.sensext = ''
    self.version = ''
    self.date = ''

  def loadEUCLIDGblueA(self):
    """
    Method to load default EUCLID/Gblue beam A configuration
    """
    self.idientier = 'A'
    
    # trace description
    self.xstart = 0
    self.xend = 392
    self.odydx = 1
    self.dydx = [0.0, 0.0]
    
    # x and y offsets
    self.xoff = -195.0
    self.yoff = 0.0
    
    # dispersion solution
    self.odldp = 1
    self.dldp = [10870.0, 9.8]
    
    # sensitivity
    self.sensitivity = 'Gblue_noDET.sens.fits'
    self.sensext = ''

  def loadEUCLIDGredA(self):
    """
    Method to load default EUCLID/Gred beam A configuration
    """
    self.idientier = 'A'
    
    # trace description
    self.xstart = 0
    self.xend = 584
    
    self.odydx = 1
    self.dydx = [0.0, 0.0]
    
    # x and y offsets
    self.xoff = -291.0
    self.yoff = 0.0
    
    # dispersion solution
    self.odldp = 1
    self.dldp = [14420.0, 9.8]
    
    # sensitivity
    self.sensitivity = 'Gred_noDET.sens.fits'
    self.sensext = ''
    self.version = ''
    self.date = ''
  
  def get_sens_output(self):
    return self.sensitivity + self.version + self.date + self.sensext
    
  def loadFromConf(self, conf, hconf=0, id='A'):
    self.idientier = conf[hconf].header['BEAMID'+str(id)]
    
    # trace description
    self.xstart = float(conf[hconf].header['BSTART'+str(id)])
    self.xend = float(conf[hconf].header['BEND'+str(id)])
    
    self.odydx = int(conf[hconf].header['ODYDX'+str(id)])
    self.dydx = []
    for i in range(self.odydx+1):
      self.dydx.append(float(conf[hconf].header['DYDX'+str(id)+'_'+str(i)]))
    
    # x and y offsets
    self.xoff = float(conf[hconf].header['XOFF'+str(id)])
    self.yoff = float(conf[hconf].header['YOFF'+str(id)])
    
    # dispersion solution
    self.odldp = int(conf[hconf].header['ODLDP'+str(id)])
    self.dldp = []
    for i in range(self.odldp+1):
      self.dldp.append(float(conf[hconf].header['DLDP'+str(id)+'_'+str(i)]))
    
    # sensitivity
    self.sensitivity = conf[hconf].header['SENS'+str(id)]
    try:
        self.version = '_v'+str(conf[self.sensitivity].header['VERSION'])
    except (KeyError, ValueError):
        self.version = ''
    try:
        self.date = '_d'+str(conf[self.sensitivity].header['DATE'])
    except (KeyError, ValueError):
        self.date = ''
    self.sensext = '.fits'

    # PSF
    try:
      self.sig1 = float(conf[hconf].header['PSFSIG1'+str(id)])
    except (KeyError, ValueError):
      self.sig1 = None
    try:
      self.sig2 = float(conf[hconf].header['PSFSIG2'+str(id)])
    except (KeyError, ValueError):
      self.sig2 = None
    try:
      self.c = float(conf[hconf].header['PSFC'+str(id)])
    except (KeyError, ValueError):
      self.c = None
   
  def printParams(self):
    """
    Method to print configuration
    """
    
    print "BEAM%s %f %f" % (self.idientier, self.xstart, self.xend)
    print "MMAG_EXTRACT_%s 35" % self.idientier
    print "MMAG_MARK_%s 35" % self.idientier
    print ""
    print "# Trace description"
    print "DYDX_ORDER_%s %d" % (self.idientier,len(self.dydx)-1)
    for i in range(len(self.dydx)):
      print "DYDX_%s_%d %f" % (self.idientier, i, self.dydx[i])
    print ""
    print "# X and Y Offsets"
    print "XOFF_%s %f" % (self.idientier,self.xoff)
    print "YOFF_%s %f" % (self.idientier,self.yoff)
    print ""
    print "# Dispersion solution"
    print "DISP_ORDER_%s %d" % (self.idientier,len(self.dldp)-1)
    for i in range(len(self.dldp)):
      print "DLDP_%s_%d %f" % (self.idientier, i, self.dldp[i])
    print ""
    print "SENSITIVITY_%s %s" % (self.idientier, self.sensitivity)
    print ""

  def close(self):
    del self.idientier
    del self.xstart
    del self.xend
    del self.dydx
    del self.xoff
    del self.yoff
    del self.dldp
    del self.sensitivity
    del self

class Grism:
  """
  Class to model a grism
  """
  
  def __init__(self):
    """
    Constructor: Initialize the class
    """
    
    self.idientier = None

    # PSF parameters
    self.lambdaRef = 0.0
    self.sig1 = 0.0
    self.sig2 = 0.0
    self.c = 0.0

    # List of beam
    self.beams = []
    self.nbeam = 0
    
  def loadEUCLIDGblue(self, rot=False):
    """
    Method to load default EUCLID/Gblue configuration
    """
    
    if rot:
        self.idientier = 'GBLUE90'
    else:
        self.idientier = 'GBLUE0'
    
    beama = Beam()
    beama.loadEUCLIDGblueA()
    
    self.beams = [beama]
    self.nbeam = 1
    
    self.lambdaRef = 1250.0
    self.sig1 = 0.12
    self.sig2 = 0.66
    self.c = 0.75
        
  def loadEUCLIDGred(self, rot=False):
    """
    Method to load default EUCLID/Gred configuration
    """
    
    if rot:
        self.idientier = 'GRED90'
    else:
        self.idientier = 'GRED0'
    
    beama = Beam()
    beama.loadEUCLIDGredA()
    self.beams = [beama]
    self.nbeam = 1

    self.lambdaRef = 1750.0
    self.sig1 = 0.15
    self.sig2 = 0.84
    self.c = 0.75

  def loadFromConf(self, conf, hconf):
    self.idientier = conf[hconf].header['CAMERA']
    
    try:
        self.lambdaRef = float(conf[hconf].header['PSFWAVE'])
    except (KeyError, ValueError):
        self.lambdaRef = None
    try:
      self.sig1 = float(conf[hconf].header['PSFSIG1'])
    except (KeyError, ValueError):
      self.sig1 = None
    try:
      self.sig2 = float(conf[hconf].header['PSFSIG2'])
    except (KeyError, ValueError):
      self.sig2 = None
    try:
      self.c = float(conf[hconf].header['PSFC'])
    except (KeyError, ValueError):
      self.c = None
   
    self.nbeam = int(conf[hconf].header['NBEAM'])
    self.beams = []
    for b in range(self.nbeam):
      self.beams.append(Beam())
      self.beams[b].loadFromConf(conf, hconf, b)

  def printParams(self):
    """
    Method to print configuration
    """
    
    print "#PSF parameters"
    print "PSFRANGE %f %f" % (self.lambdaRef, self.lambdaRef)
    print "PSFCOEFFS 1.0"
    print "PSFSIG1 %f" % self.sig1
    print "PSFSIG2  %f" % self.sig2
    print "PSFC  %f" % self.c
    print ""
    print "#Beam parameters"
    for b in self.beams:
      b.printParams()
    print ""

  def close(self):
    del self.idientier
    del self.lambdaRef
    del self.sig1
    del self.sig2
    del self.c

    if len(self.beams)>0:
      for i in range(len(self.beams)):
        self.beams[i].close()
    del self.beams
    del self

class Spectrometer:
  """
  Class to model a spectro = grism + det
  """
  
  def __init__(self):
    """
    Constructor: Initialize the class
    """
    
    self.idientier = None
    
    self.telarea = 0.0
    self.exptime = 0.0
    self.expname = None
    
    self.wcs = None    
    self.llim = None
    self.rlim = None
    self.ulim = None
    self.dlim = None
    
    self.detector = Detector()
    
    self.rot90 = False
    self.grism = Grism()
    
    self.skyAbs = None
    self.skyBck = None
    
    self.version = ''
    self.model = ''
    self.date = ''

  def loadEUCLIDGblue0(self, detId=1, wcs=None, exptime=None):
    """
    Method to load default EUCLID/Gblue 0 deg configuration
    """
    
    self.idientier = 'NISP'
    
    self.telarea = 10066.0
    
    if exptime==None:
        self.exptime = 560.0
    else:
        self.exptime = exptime
    self.rot90 = False
    self.detector.loadEUCLIDdefault(detId)
    self.grism.loadEUCLIDGblue(rot=self.rot90)
    
    if wcs == None:
        self.wcs = WCSObject()
    else:
        self.wcs = copy.copy(wcs)
    
  def loadEUCLIDGred0(self, detId=1, wcs=None, exptime=None):
    """
    Method to load default EUCLID/Gred configuration
    """
    
    self.idientier = 'NISP'
    
    self.telarea = 10066.0
        
    if exptime==None:
        self.exptime = 560.0
    else:
        self.exptime = exptime
    self.rot90 = False
    self.detector.loadEUCLIDdefault(detId)
    self.grism.loadEUCLIDGred(rot=self.rot90)
    
    if wcs == None:
        self.wcs = WCSObject()
    else:
        self.wcs = copy.copy(wcs)
        
  def loadEUCLIDGblue90(self, detId=1, wcs=None, exptime=None):
    """
    Method to load default EUCLID/Gblue 90 deg configuration
    """
    
    self.idientier = 'NISP'
    
    self.telarea = 10066.0
    
    if exptime==None:
        self.exptime = 560.0
    else:
        self.exptime = exptime
    self.rot90 = True
    self.detector.loadEUCLIDdefault(detId)
    self.grism.loadEUCLIDGblue(rot=self.rot90)
    
    if wcs == None:
        self.wcs = WCSObject()
    else:
        self.wcs = copy.copy(wcs)
    
  def loadEUCLIDGred90(self, detId=1, wcs=None, exptime=None):
    """
    Method to load default EUCLID/Gred configuration
    """
    
    self.idientier = 'NISP'
    
    self.telarea = 10066.0
    
    if exptime==None:
        self.exptime = 560.0
    else:
        self.exptime = exptime
    self.rot90 = True
    self.detector.loadEUCLIDdefault(detId)
    self.grism.loadEUCLIDGred(rot=self.rot90)
    
    if wcs == None:
        self.wcs = WCSObject()
    else:
        self.wcs = copy.copy(wcs)
        
  def loadFromConf(self, conf, hconf=0, detId=1, wcs=None, exptime=None):
    self.idientier = conf[0].header['INSTRU']
    self.telarea = float(conf[0].header['TELAREA'])
    self.detector.loadFromConf(conf, hconf, detId)
    self.grism.loadFromConf(conf, hconf)
    self.rot90 = bool(conf[hconf].header['ROT90'])

    # sky projection parameters
    if wcs == None:
        self.wcs = WCSObject()
    else:
        self.wcs = copy.copy(wcs)
    
    if exptime == None:
        self.exptime = float(conf[hconf].header['EXPTIME'])
    else:
        self.exptime = exptime
        
    # set sky backgroud and sky absortion
    try:
        self.skyBck = conf[hconf].header['SKYBCK']
    except (KeyError, ValueError):
        self.skyBck = conf[0].header['SKYBCK']

    # the sky absorption is not fully implemented
    # feature disable for know
    #self.skyAbs = conf['SKYABS']
    self.skyAbs = None   
    
    # set the version name
    try:
        self.version = '_v'+str(conf[0].header['VERSION'])
    except (KeyError, ValueError):
        self.version = ''
    try:
        self.model = '_'+str(conf[0].header['MODEL'])
    except (KeyError, ValueError):
        self.model = ''       
    try:
        self.date = '_d'+str(conf[0].header['DATE'])
    except (KeyError, ValueError):
        self.date = ''
        
    try:
        self.expname = str(conf[hconf].header['EXTNAME'])
    except (KeyError, ValueError):
        self.expname = None
        
  def printParams(self):
    """
    Method to print configuration
    """
    print "INSTRUMENT %s" % self.idientier
    print "CAMERA %s" % self.grism.idientier
    print ""
    print "# WCS parameters"
    print "CRPIX1 %f" % (self.wcs.crpix1)
    print "CRPIX2 %f" % (self.wcs.crpix2)
    print "CRVAL1 %f" % (self.wcs.crval1)
    print "CRVAL2 %f" % (self.wcs.crval2)
    print "CD1_1 %e" % (self.wcs.cd11)
    print "CD1_2 %e" % (self.wcs.cd12)
    print "CD2_1 %e" % (self.wcs.cd21)
    print "CD2_2 %e" % (self.wcs.cd22)
    print "ORIENTAT %f" % (self.wcs.orient)
    print ""
    
    self.detector.printParams()
    
    print "TELAREA %f" % self.telarea
    print "POBJSIZE 0.1"
    print "SMFACTOR 1.0"
    self.grism.printParams()
    
  def writeaXeConf(self, filename):
    """
    Method to write conf in a file in aXe format
    """
    toWrite="INSTRUMENT %s\n" % self.idientier
    toWrite+="CAMERA %s\n" % self.grism.idientier
    toWrite+="EXPTIME %f\n" % self.exptime
    toWrite+="\n"
    toWrite+="# Outout format\n"
    toWrite+="SCIENCE_EXT SCI ; Science extension\n"
    toWrite+="DQ_EXT DQ       ; DQ extension\n"
    toWrite+="ERRORS_EXT ERR  ; Error extension\n"
    toWrite+="\n"
    toWrite+="# WCS parameters\n"
    toWrite+="CRPIX1 %f\n" % (self.wcs.crpix1)
    toWrite+="CRPIX2 %f\n" % (self.wcs.crpix2)
    toWrite+="CRVAL1 %f\n" % (self.wcs.crval1)
    toWrite+="CRVAL2 %f\n" % (self.wcs.crval2)
    toWrite+="CD1_1 %e\n" % (self.wcs.cd11)
    toWrite+="CD1_2 %e\n" % (self.wcs.cd12)
    toWrite+="CD2_1 %e\n" % (self.wcs.cd21)
    toWrite+="CD2_2 %e\n" % (self.wcs.cd22)
    toWrite+="ORIENTAT %f\n" % (self.wcs.orient)
    toWrite+="\n"
    toWrite+="# pixels properties\n"
    toWrite+="RDNOISE %s\n" % (self.detector.get_map_output('RN'))
    toWrite+="DC %s\n" % (self.detector.get_map_output('DC'))
    toWrite+="QE %s\n" % (self.detector.get_map_output('QE'))
    toWrite+="NPIXX %d\n" % (self.detector.nx)
    toWrite+="NPIXY %d\n" % (self.detector.ny)
    toWrite+="FFNAME %s\n" % (str(self.detector.ffname))
    toWrite+="EXPNAME %s\n" % (str(self.detector.expname))
    toWrite+="NBIT %s\n" % (str(self.detector.nbit))
    toWrite+="COSMAP %s\n" % (self.detector.get_map_output('COS'))
    toWrite+="REJECT %s\n" % (str(self.detector.reject))
    toWrite+="RDMODE %s\n" % (str(self.detector.rdmode))
    toWrite+="\n"
    toWrite+="#PSF parameters\n"
    toWrite+="TELAREA %f\n" % self.telarea
    toWrite+="POBJSIZE 0.1\n"
    toWrite+="SMFACTOR 1.0\n"
    toWrite+="PSFRANGE %f %f\n" % (self.grism.lambdaRef, self.grism.lambdaRef)
    toWrite+="PSFCOEFFS 1.0\n"
    if self.grism.sig1 != None:
      toWrite+="PSFSIG1 %f\n" % (self.grism.sig1/self.detector.scale)
    if self.grism.sig2 != None:
      toWrite+="PSFSIG2  %f\n" % (self.grism.sig2/self.detector.scale)
      toWrite+="PSFC  %f\n" % self.grism.c
    toWrite+="\n"
    toWrite+="#Beam parameters\n"
    for b in self.grism.beams:
        toWrite+="BEAM%s %f %f\n" % (b.idientier, b.xstart, b.xend)
        toWrite+="MMAG_EXTRACT_%s 35\n" % b.idientier
        toWrite+="MMAG_MARK_%s 35\n" % b.idientier
        toWrite+="\n"
        if b.sig1 != None:
          toWrite+="PSFSIG1%s %f\n" % (b.idientier, b.sig1/self.detector.scale)
        if b.sig2 != None:
          toWrite+="PSFSIG2%s %f\n" % (b.idientier, b.sig2/self.detector.scale)
          toWrite+="PSFC%s %f\n" % (b.idientier, b.c)
        toWrite+="\n"
        toWrite+="# Trace description\n"
        toWrite+="DYDX_ORDER_%s %d\n" % (b.idientier,b.odydx)
        for i in range(len(b.dydx)):
          toWrite+="DYDX_%s_%d %f\n" % (b.idientier, i, b.dydx[i])
        toWrite+="\n"
        toWrite+="# X and Y Offsets\n"
        toWrite+="XOFF_%s %f\n" % (b.idientier,b.xoff)
        toWrite+="YOFF_%s %f\n" % (b.idientier,b.yoff)
        toWrite+="\n"
        toWrite+="# Dispersion solution\n"
        toWrite+="DISP_ORDER_%s %d\n" % (b.idientier,b.odldp)
        for i in range(len(b.dldp)):
          toWrite+= "DLDP_%s_%d %f\n" % (b.idientier, i, b.dldp[i])
        toWrite+="\n"
        toWrite+="SENSITIVITY_%s %s\n" % (b.idientier, b.get_sens_output())
        toWrite+="\n"

    file = open(filename, 'w')
    file.write(toWrite)
    file.close()

  def close(self):
    del self.idientier
    del self.telarea
    del self.exptime
    if self.skyBck != None:
        try: 
            test=float(self.skyBck)
            del self.skyBck
        except ValueError:
            self.skyBck.close()
    if self.skyAbs != None:
        try:
            test=float(self.skyAbs)
            del self.skyAbs
        except ValueError:
            self.skyAbs.close()
    if self.wcs != None:
        self.wcs.close()
    else:
        del self.wcs
    del self.rot90
    if self.detector != None:
      self.detector.close()
    else:
      del self.detector
    if self.grism != None:
      self.grism.close()
    else:
      del self.detector
    del self

class WCSObject:
    """ 
    This class should contain the WCS information
    """
    
    def __init__(self):
        self.orient = 0.0       
        self.pscale = 0.0           
        self.crpix1 = 0.0
        self.crpix2 = 0.0
        self.crval1 = 0.0
        self.crval2 = 0.0
        self.cd11 = 0.3/3600.0
        self.cd12 = 0.0
        self.cd21 = 0.0
        self.cd22 = 0.3/3600.0
        self.npix1 = 2040.0
        self.npix2 = 2040.0
        
    def _deg2rad(self, deg):
        return (deg * numpy.pi / 180.)

    def _rad2deg(self, rad):
        return (rad * 180. / numpy.pi)
        
    def _divmod(self, num, val):
        if isinstance(num,numpy.ndarray):
            # Treat number as numpy object
            _num = numpy.remainder(num,val)
        else:
            _num = divmod(num,val)[1]
        return _num

    def updateWCS(self, pixel_scale=None, orient=None,refpos=None,refval=None, size=None):
        """
        Create a new CD Matrix from the absolute pixel scale
        and reference image orientation.
        """
        # Set up parameters necessary for updating WCS
        # Check to see if new value is provided,
        # If not, fall back on old value as the default

        _updateCD = False
        if orient != None:
            pa = self._deg2rad(orient)
            self.orient = orient
            _updateCD = True
        else:
            # In case only pixel_scale was specified
            pa = self._deg2rad(self.orient)
       
        if pixel_scale != None:
            self.pscale = pixel_scale
            _updateCD = True
        else:
            # In case, only orient was specified
            pixel_scale = self.pscale

        if refpos != None:
            self.crpix1 = refpos[0]
            self.crpix2 = refpos[1]

        if refval != None:
            self.crval1 = refval[0]
            self.crval2 = refval[1]

        if size != None:
            self.npix1 = size[0]
            self.npix2 = size[1]

        # Reset WCS info now...
        if _updateCD:
            # Only update this should the pscale or orientation change...
            pscale = pixel_scale / 3600.
            #self.cd11 = -pscale * numpy.cos(pa) 
            #self.cd12 = pscale * numpy.sin(pa) 
            #self.cd21 = self.cd12 
            #self.cd22 = -self.cd11 
            self.cd11 = pscale * numpy.cos(pa)
            self.cd12 = pscale * numpy.sin(pa)
            self.cd21 = -pscale * numpy.sin(pa)
            self.cd22 = pscale * numpy.cos(pa)

    def xy2rd(self,x, y):
        """
        This method would apply the WCS keywords to a position to
        generate a new sky position.

        The algorithm comes directly from wcsutils

        translate (x,y) to (ra, dec)
        """           
        xi = self.cd11 * (x - self.crpix1) + self.cd12 * (y - self.crpix2)
        eta = self.cd21 * (x - self.crpix1) + self.cd22 * (y - self.crpix2)

        xi = self._deg2rad(xi)
        eta = self._deg2rad(eta)
        ra0 = self._deg2rad(self.crval1)
        dec0 = self._deg2rad(self.crval2)

        ra = numpy.arctan((xi / (numpy.cos(dec0)-eta*numpy.sin(dec0)))) + ra0
        dec = numpy.arctan( ((eta*numpy.cos(dec0)+numpy.sin(dec0)) /
                (numpy.sqrt((numpy.cos(dec0)-eta*numpy.sin(dec0))**2 + xi**2))) )

        ra = self._rad2deg(ra)
        dec = self._rad2deg(dec)
        ra = self._divmod(ra, 360.)
        
        return ra,dec


    def rd2xy(self,ra_deg, dec_deg):
        """
        This method would use the WCS keywords to compute the XY position
        from a given RA/Dec (in deg).
        """
        det = self.cd11*self.cd22 - self.cd12*self.cd21
        
        if det == 0.0:
            error_message = "Error in WCSObject : Singular CD matrix!"
            raise TIPSError(error_message)
        
        cdinv11 = self.cd22 / det
        cdinv12 = -self.cd12 / det
        cdinv21 = -self.cd21 / det
        cdinv22 = self.cd11 / det

        # translate (ra, dec) to (x, y)
        ra0 = self._deg2rad(self.crval1)
        dec0 = self._deg2rad(self.crval2)
        ra = self._deg2rad(ra_deg)
        dec = self._deg2rad(dec_deg)
        
        bottom = numpy.sin(dec)*numpy.sin(dec0) + numpy.cos(dec)*numpy.cos(dec0)*numpy.cos(ra-ra0)
        
        if isinstance(bottom,numpy.ndarray):
            isbadbottom = (not len(numpy.nonzero(bottom)[0]) == len(bottom))
        else:
            isbadbottom = (bottom == 0.0)

        if isbadbottom:
            error_message = "Error in WCSObject : Unreasonable RA/Dec range!"
            raise TIPSError(error_message)

        xi_rad = numpy.cos(dec) * numpy.sin(ra-ra0) / bottom
        eta_rad = (numpy.sin(dec)*numpy.cos(dec0) - numpy.cos(dec)*numpy.sin(dec0)*numpy.cos(ra-ra0)) / bottom
        xi = self._rad2deg(xi_rad)
        eta = self._rad2deg(eta_rad)
        
        x = cdinv11 * xi + cdinv12 * eta + self.crpix1
        y = cdinv21 * xi + cdinv22 * eta + self.crpix2

        return x,y

    def _buildRotMatrix(self,theta):
        _theta = self._deg2rad(theta)
        _mrot = numpy.zeros(shape=(2,2),dtype=numpy.float32)
        _mrot[0] = (numpy.cos(_theta),numpy.sin(_theta))
        _mrot[1] = (-numpy.sin(_theta),numpy.cos(_theta))

        return _mrot

    def rotateCD(self,delta,centered=False):
        """ Rotates WCS CD matrix
        """
        if delta == 0.:
            return
            
        if centered:
            if self.npix1==0.0 or self.npix2==0.0:
                error_message = "Error in WCSObject : Size need to set to compute a centered rotatation!"
                raise TIPSError(error_message)
            (_racent, _deccent) = self.xy2rd(self.npix1/2.0, self.npix2/2.0)
            
        # Start by building the rotation matrix...
        _rot = self._buildRotMatrix(delta)
        # ...then, rotate the CD matrix and update the values...
        _cd = numpy.array([[self.cd11,self.cd12],[self.cd21,self.cd22]])
        _cdrot = numpy.dot(_cd,_rot)
        self.cd11 = _cdrot[0][0]
        self.cd12 = _cdrot[0][1]
        self.cd21 = _cdrot[1][0]
        self.cd22 = _cdrot[1][1]
        self.orient = self.orient + delta
        
        if centered:
            (_ranew, _decnew) = self.xy2rd(self.npix1/2.0, self.npix2/2.0)
            _raoff = _racent - _ranew
            _decoff = _deccent - _decnew
            self.crval1 += _raoff
            self.crval2 += _decoff
            
    def close(self):
        del self.orient
        del self.pscale           
        del self.crpix1
        del self.crpix2
        del self.crval1
        del self.crval2
        del self.cd11
        del self.cd12
        del self.cd21
        del self.cd22
        del self.npix1
        del self.npix2

        del self

class FocalPlan:
  """
  Class to simulate a focale plan
  """
  
  def __init__(self):
    """
    Constructor: init the class
    """
    
    self.spectros = []
    
    self.xstep = 0.0
    self.ystep = 0.0
    
    self.fovlim = None
    
    self.skyBck = None
    self.skyAbs = None
    
  def setSkyBck(self, value):
      for s in range(len(self.spectros)):
            self.spectros[s].skyBck = value
      
  def loadEUCLIDDefault(self, ra0=0.0, dec0=0.0, orient=0.0, grism = 'Gblue0', exptime=0.0, x0=0.0, y0=0.0):
    """
    Method to load EUCLID default focal plan
    """
    
    self.xstep = 3000.0/18.0 #pix
    self.ystep = 6000.0/18.0 #pix
    
    self.spectros = []
    
    # init wcs Object for the focal plan
    wcs0 = WCSObject()
    wcs0.updateWCS(pixel_scale=0.3, orient=orient,refpos=[x0, y0],refval=[ra0,dec0], size=[2040., 2040.])
    
    index = 0
    for i in range(4):
      for j in range(4):
        self.spectros.append(Spectrometer())
        
        did = str(i)+str(j)

        # set wcs for the current dectector
        xref = float(i)*(2040.+self.xstep)
        yref = float(j)*(2040.+self.ystep)
        (raref, decref) = wcs0.xy2rd(xref, yref)
        wcs = copy.copy(wcs0)
        wcs.updateWCS(refval=[raref,decref])
        
        if grism == 'Gblue0':
          self.spectros[index].loadEUCLIDGblue0(detId=did, wcs=wcs, exptime=exptime)
        elif grism == 'Gblue90':
          self.spectros[index].loadEUCLIDGblue90(detId=did, wcs=wcs, exptime=exptime)
        elif grism == 'Gred0':
          self.spectros[index].loadEUCLIDGred0(detId=did, wcs=wcs, exptime=exptime)
        elif grism == 'Gred90':
          self.spectros[index].loadEUCLIDGred90(detId=did, wcs=wcs, exptime=exptime)
        else:
          error_message = 'Can not load grism: '+grism
          raise TIPSError(error_message)
        
        index += 1
        
  def loadFromConf(self, conf, hconf, ra0, dec0, orient=0.0, exptime=None, x0=0.0, y0=0.0):
    pixsize = float(conf[0].header['PIXSIZE'])
    pixscale = float(conf[0].header['PIXSCALE'])
    npixx = float(conf[0].header['NPIXX'])
    npixy = float(conf[0].header['NPIXY'])
    
    if len(self.spectros)==0:
        self.ndetx = int(conf[0].header['NDETX'])
        self.ndety = int(conf[0].header['NDETY'])
        self.xstep = float(conf[0].header['XSTEP'])/pixsize
        self.ystep = float(conf[0].header['YSTEP'])/pixsize
        try:
            self.fovlim = float(conf[0].header['FOVLIM'])/pixsize
        except (KeyError, ValueError):
            self.fovlim = None   
    
    # init wcs Object for the focal plan
    wcs0 = WCSObject()
    wcs0.updateWCS(pixel_scale=pixscale, orient=orient,refpos=[x0, y0],refval=[ra0,dec0], size=[npixx, npixy])
    
    for i in range(self.ndetx):
      for j in range(self.ndety):
        self.spectros.append(Spectrometer())
        did = str(i)+str(j)
        
        # set wcs for the current dectector
        xref = float(i)*(npixx+self.xstep)
        yref = float(j)*(npixy+self.ystep)
        (raref, decref) = wcs0.xy2rd(xref, yref)
        wcs = copy.copy(wcs0)
        wcs.updateWCS(refval=[raref,decref])
        
        self.spectros[-1].loadFromConf(conf, hconf=hconf, detId=did, wcs=wcs, exptime=exptime)
        if self.fovlim != None:
            if i==0:
                self.spectros[-1].llim = -self.fovlim
            if i==(self.ndetx-1):
                self.spectros[-1].rlim = npixx+self.fovlim
            if j==0:
                self.spectros[-1].dlim = -self.fovlim
            if j==(self.ndety-1):
                self.spectros[-1].ulim = npixy+self.fovlim

  def close(self):
    if len(self.spectros)>0:
      for i in range(len(self.spectros)):
        self.spectros[i].close()
    del self.spectros
    del self.xstep
    del self.ystep
    del self
