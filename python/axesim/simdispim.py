"""
$Revision: 1.2 $ $Date: 2009/09/21 12:46:17 $
Author: Martin Kuemmel (mkuemmel@stecf.org)
Affiliation: Space Telescope - European Coordinating Facility
WWW: http://www.stecf.org/software/slitless_software/axesim/
Modified by Julien Zoubian
"""
import shutil
import pyfits
import numpy
import sys

import scipy
from scipy import interpolate
from scipy import ndimage
from scipy.ndimage import filters
from scipy.ndimage.filters import gaussian_filter
 
import imagemaker
import modspeclist
import axecommands
import realworld
import configfile

from axesimerror  import *
from axesimutils  import *
from inputchecker import *

def addImages(img1_path, img2_path, c=None):
      # combine the images
      img1 = pyfits.open(img1_path, mode='update')
      img2 = pyfits.open(img2_path)
      signal1 = numpy.asarray(img1['SCI'].data)
      signal2 = numpy.asarray(img2['SCI'].data)
      if c==None:
        coef1 = 1.0
        coef2 = 1.0
      else:
        coef1 = c
        coef2 = (1-c)
      signal = (coef1*signal1) + (coef2*signal2)
      img1['SCI'].data = signal
      img1.flush()
      img1.close()
      img2.close()

def addBeams(img_list):
      # combine the images
      img1 = pyfits.open(img_list[0], mode='update')
      signal = numpy.asarray(img1['SCI'].data)
      for img2_path in img_list[1:]:
        img2 = pyfits.open(img2_path)
        signal += numpy.asarray(img2['SCI'].data)
        img2.close()
        os.unlink(img2_path)
      img1['SCI'].data = signal
      img1.flush()
      img1.close()

def simOne(confile, psfsig, psfwave, nx, ny, modCat, modSpc, modImg, randRoot='t'):
    # make a full path to the
    # direct image as dummy and as final output
    dummy_grisima_path = putIMAGE(get_random_filename(randRoot, '_DISP.fits'))

    dummy_incat_path = putIMAGE(get_random_filename(randRoot, '.cat'))
    shutil.copy(putIMAGE(modCat), dummy_incat_path)
    
    # create the dummy image maker
    i_maker = imagemaker.DummyImages(putCONF(confile), dummy_grisima_path, None, nx, ny)
    i_maker.makeImages()

    # load the model object table
    inobjects = modspeclist.ModelObjectTable(dummy_incat_path, modSpc, modImg)
    # fill the model object table
    inobjects.fill_columns(i_maker.WCSimage, i_maker.WCSext, psfsig)

    # load the object to make the grism simulations
    grismator = axecommands.DispImator(i_maker, confile, dummy_incat_path,
                                       psfwave, modSpc, modImg)
    grismator.run()

    grismator.mopup()
    os.unlink(dummy_incat_path)
    
    return dummy_grisima_path

def doubleGaussConv(data, sigma1, sigma2, c, smpfac):
    if sigma1 == None:
        return data
    elif sigma2 == None:
        return gaussian_filter(data, sigma1*smpfac, order=0, mode='nearest')
    else:
        tdata1 = gaussian_filter(data, sigma1*smpfac, order=0, mode='nearest')
        tdata2 = gaussian_filter(data, sigma2*smpfac, order=0, mode='nearest')
        return (c*tdata1) + ((1-c)*tdata2)

def resample(data, smpfac):
    if smpfac > 1.0-1.0e-10 and smpfac < 1.0+1.0e-10:
        return data
    else:
        xlen = len(data)
        ylen = len(data[0])
        nxlen = int(float(xlen)/smpfac)
        nylen = int(float(ylen)/smpfac)
        
        x = numpy.arange(xlen)
        y = numpy.arange(ylen)
        xnew = numpy.arange(0, xlen, smpfac)
        ynew = numpy.arange(0, ylen, smpfac)
        
        f = interpolate.interp2d(x, y, data, kind='quintic')
        znew = f(xnew, ynew)
        return znew/znew.sum()

def prepModImg(modimg_path, sigma1, sigma2, c, randRoot='t'):
  
    # load model image
    dummy_modimg_path = get_random_filename(randRoot, '_MOD.fits')
    inModImg = pyfits.open(putIMAGE(modimg_path))
    outModImg = pyfits.HDUList()
    outModImg.append(pyfits.PrimaryHDU())
    
    # loop on model images
    irange = xrange(1, len(inModImg))
    for i in irange:
        # load image
        data = numpy.asarray(inModImg[i].data)
        
        # get sampling factor
        try:
            smpfac = float(inModImg[i].header['SMPFAC'])
            if smpfac <= 0.0:
                error_message = 'Sampling factor must be positive: %f' % smpfac
                raise aXeSIMError(error_message)
        except KeyError, ValueError:
            smpfac = 1.0
    
        # convolve with PSF
        ndata = doubleGaussConv(data, sigma1, sigma2, c, smpfac)

        # resample if needed
        rdata = resample(ndata, smpfac)
        
        outModImg.append(pyfits.ImageHDU(rdata))
        
    outModImg.writeto(putIMAGE(dummy_modimg_path))
    return dummy_modimg_path
            
def simdispim(incat=None, config=None, dispim_name=None, exptime=None,
              model_spectra=None, model_images=None, bck_flux=0.0,
              silent=True, debug=False, detector=True,
              norm=True):
    """
    Main function for the task SIMDISPIM

    This module is the high level wrapper function for the
    task SIMDISPIM. All necessary actions are done, feedback
    is given to the user

    @param incat: name of model object table
    @type incat: string
    @param config: aXe configuration file name
    @type config: string
    @param dispim_name: name of dispersed image
    @type dispim_name: string
    @param model_spectra: name of model spectra file
    @type model_spectra: string
    @param model_images: name of model images
    @type model_image: string
    @param bck_flux: flux in background
    @type bck_flux: float
    @param silent: flag for silent run
    @type silent: boolean
    @param debug: print debug output if true
    @type debug: boolean
    @param detector: add detector noise if true
    @type detector: boolean
    @param norm: normalize image with exposure time if True
    @type norm: boolean
    """
    
    if silent:
        stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        
    # give brief feedback
    print '\nSIMDISPIM: Starting ...'

    # just set the environments
    get_environments()

    if config==None:
        print __doc__
        return 1

    if incat == None and (model_images != None or model_spectra != None):
        error_message = 'incat is not defined.'
        print __doc__
        return 1
       
    # check the input parameters
    in_check = InputChecker()
    # for the 'simdisp'-task
    in_check.check_simdispim_input(incat, config, model_spectra, model_images, bck_flux)

    if dispim_name == None:
        if incat == None:
            error_message = 'Both dispim_name and incat or not defined'
            raise aXeSIMError(error_message)
        else:
            # derive the output name
            pos = incat.rfind('.')
            if pos < 0:
                root = incat
            else:
                root = incat[:pos]
    else:
        root = dispim_name.replace('.fits','')
    
    dirima_name  = root + '_direct.fits'
    grisima_name = root + '.fits'
    
    final_dirima_path  = putOUTSIM(dirima_name)
    final_grisima_path = putOUTSIM(grisima_name)

    # load the aXe configuration file
    conf = configfile.ConfigFile(putCONF(config))

    # load exptime-value
    if exptime == None:
      exptime = float(conf.get_gvalue('EXPTIME'))
    if exptime != None and exptime < 0:
      error_message = 'Value for "exptime" or "exptime_disp" most be positive: ' + str(exptime)
      raise aXeSIMError(error_message)

    # load lambda_psf 
    lambda_psf = conf.confirm_lambda_psf()

    # load nx-value
    nx = int(conf.get_gvalue('NPIXX'))
    if nx != None and nx <= 0.0:
      error_message = 'Value for "nx" or "nx_disp" most be positive: ' + str(nx)
      raise aXeSIMError(error_message)

    # load ny-value
    ny = int(conf.get_gvalue('NPIXY'))
    if ny != None and ny <= 0:
      error_message = 'Value for "ny" or "ny_disp" most be positive: ' + str(ny)
      raise aXeSIMError(error_message)
    if incat != None:
        print 'SIMDISPIM: Input Model Object List:       %s' % putIMAGE(incat)
    print 'SIMDISPIM: Input aXe configuration file:  %s' % putCONF(config)
    if model_spectra != None:
        print 'SIMDISPIM: Input Model Spectra:           %s' % putIMAGE(model_spectra)
    if model_images != None:
        print 'SIMDISPIM: Input Model Image:             %s' % putIMAGE(model_images)
    print 'SIMDISPIM: Fixed wavlength for PSF:       %s' % str(lambda_psf)
    if exptime != None:
        print 'SIMDISPIM: Input exposure time:           %s' % str(exptime)
    if nx == None and ny == None:
        print 'SIMDISPIM: Input image dimensions:        %s' % 'AUTO'
    else:
        print 'SIMDISPIM: Input image dimensions:        (%s,%s)' % (str(nx),str(ny))

    print 'SIMDISPIM: Output dispersed image:        %s' % final_grisima_path

    print ''
   
    dummy_grisima_list = []
    for beam in conf.beams:
      # make the simulation configuration
      # file pointing the correct extensions
      config_simul = conf.axesim_prep(beam)

      # load the simulation configuration file
      conf_simul = configfile.ConfigFile(putCONF(config_simul))
      
      # load PSFSIG1-value
      psfkey = 'PSFSIG1'+beam
      if conf.beams[beam].get_bvalue(psfkey) != None:
        psfsig1 = float(conf.beams[beam].get_bvalue(psfkey))
        print 'SIMDISPIM: Sigma PSF %s:                   %f' % (beam, psfsig1)
      elif conf_simul.get_gvalue('PSFSIG1') != None:
        psfsig1 = float(conf_simul.get_gvalue('PSFSIG1'))
        print 'SIMDISPIM: Sigma PSF:                     %f' % psfsig1
      else:
        psfsig1=None
 
      # load PSFSIG2-value is exist
      psfkey = 'PSFSIG2'+beam
      if conf.beams[beam].get_bvalue(psfkey) != None:
        psfsig2 = float(conf.beams[beam].get_bvalue(psfkey))
        print 'SIMDISPIM: Sigma PSF %s:                   %f' % (beam, psfsig2)
      elif conf_simul.get_gvalue('PSFSIG2') != None:
        psfsig2 = float(conf_simul.get_gvalue('PSFSIG2'))
        print 'SIMDISPIM: Sigma PSF:                     %f' % psfsig2
      else:
        psfsig2=None       
        
      psfkey = 'PSFC'+beam
      if conf.beams[beam].get_bvalue(psfkey) != None:
        psfc = float(conf.beams[beam].get_bvalue(psfkey))
        print 'SIMDISPIM: C PSF %s:                       %f' % (beam, psfc)
      elif conf_simul.get_gvalue('PSFC') != None:
        psfc = float(conf_simul.get_gvalue('PSFC'))
        print 'SIMDISPIM: C PSF:                         %f' % psfc
      else:
        psfc=None
      
      if psfsig1 != None and psfsig1 < 0:
            error_message = 'Value for "PSFSIG1" most be positive: ' + str(psfsig1)
            raise aXeSIMError(error_message)     
      if psfsig2 != None and psfsig2 < 0:
            error_message = 'Value for "PSFSIG2" most be positive: ' + str(psfsig2)
            raise aXeSIMError(error_message)
      if psfsig2 != None and psfsig1 == None:
            error_message = 'Value for "PSFSIG1" is not defined'
            raise aXeSIMError(error_message)
      if psfc != None and (psfc < 0 or psfc > 1):
            error_message = 'Value for "PSFC" most be positive and smaller than 1.0: ' + str(psfc)
            raise aXeSIMError(error_message)            
      if psfc == None and psfsig2 != None:
            error_message = 'Value for "PSFC" is not defined'
            raise aXeSIMError(error_message)
      if psfc != None and psfsig2 == None:
            error_message = 'Value for "PSFSIG2" is not defined'
            raise aXeSIMError(error_message)     
      
      if incat != None:
        if model_images != None:
           # check scipy version and print warning is < 0.12
           scipy_version = (scipy.__version__).split('.')
           if int(scipy_version[0])<1 and int(scipy_version[1])<12:
               print "WARNING : scipy version = %s and thumbnails is currently not supported for  scipy version < 0.12.0" % scipy.__version__
           modImgPath = prepModImg(model_images, psfsig1, psfsig2, psfc, randRoot=root)
           dummy_grisima_path1 = simOne(config_simul, psfsig1, lambda_psf, nx, ny, incat, model_spectra, modImgPath, randRoot=root)
           if debug:
              shutil.copy(dummy_grisima_path1, final_grisima_path.replace('.fits', '_BEAM'+beam+'.fits'))
              shutil.copy(modImgPath, final_grisima_path.replace('.fits', '_BEAM'+beam+'_MODIMG.fits'))
           os.unlink(putIMAGE(modImgPath))
        else:
          dummy_grisima_path1 = simOne(config_simul, psfsig1, lambda_psf, nx, ny, incat, model_spectra, None, randRoot=root)
          if debug:
              shutil.copy(dummy_grisima_path1, final_grisima_path.replace('.fits', '_PSF1_BEAM'+beam+'.fits'))
          if psfsig2 != None:
              dummy_grisima_path2 = simOne(config_simul, psfsig2, lambda_psf, nx, ny, incat, model_spectra, None, randRoot=root)
              if debug:
                  shutil.copy(dummy_grisima_path2, final_grisima_path.replace('.fits', '_PSF2_BEAM'+beam+'.fits'))
          
              addImages(dummy_grisima_path1, dummy_grisima_path2, psfc)
              if debug:
                  shutil.copy(dummy_grisima_path1, final_grisima_path.replace('.fits', '_BEAM'+beam+'.fits'))
              os.unlink(dummy_grisima_path2)
              
        dummy_grisima_list.append(dummy_grisima_path1)
        
        del conf_simul
        print ''
        
        # sum beams
        dummy_grisima_path = dummy_grisima_list[0]
        if len(dummy_grisima_list)>1:
          addBeams(dummy_grisima_list)
        
        if debug:
          shutil.copy(dummy_grisima_path, final_grisima_path.replace('.fits', '_nodet.fits'))
      else:
        # make a full path to the
        # direct image as dummy and as final output
        dummy_grisima_path = putIMAGE(get_random_filename(root, '_DISP.fits'))
        
        # create the dummy image maker
        i_maker = imagemaker.DummyImages(putCONF(config_simul), dummy_grisima_path, None, nx, ny)
        i_maker.makeImages()

    # convert the image into
    # a full output image with three extensions
    # and noise (if desired)
    rworld = realworld.RealWorld(dummy_grisima_path, extname='SCI', exptime=exptime,
                                 bck_flux=bck_flux, qe=conf['QE'], dc=conf['DC'], rn=conf['RDNOISE'],
                                 instrument=conf['INSTRUMENT'], detector=detector, cmap=conf['COSMAP'],
                                 reject=conf['REJECT'], nbit=conf['NBIT'], norm=norm, rdmode=conf['RDMODE'], 
                                 ngrp=conf['NGRP'], nfrm=conf['NFRM'], dtgrp=conf['DTGRP'], dtfrm=conf['DTFRM'])
    rworld.make_real()

    # move the resulting image to the correct
    # name and place
    shutil.move(dummy_grisima_path, final_grisima_path)

    # delete the object
    # explicitly
    del conf

    # give brief feedback
    print ''
    print 'SIMDISPIM: Done'
    print ''
    
    if silent:
        sys.stdout.close()
        sys.stdout = stdout

    return 0
