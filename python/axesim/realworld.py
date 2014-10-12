"""
$Revision: 1.1 $ $Date: 2008/09/05 08:01:40 $
Author: Martin Kuemmel (mkuemmel@stecf.org)
Affiliation: Space Telescope - European Coordinating Facility
WWW: http://www.stecf.org/software/slitless_software/axesim/
"""
import os
import os.path
#from pyraf import iraf
#from iraf import artdata
import pyfits
import numpy
from scipy import stats

from axesimerror import *
from axesimutils import *

class RealWorld(object):
    """
    Class for to add poisson noise
    """
    def __init__(self, image_name, extname='0', exptime=1.0, bck_flux=0.0,
                 qe=None, dc=None, rn=None, instrument=None, detector=True,
                 cmap=None, reject=None, nbit=None, norm=True, rdmode=None,
                 ngrp=None, nfrm=None, dtgrp=None, dtfrm=None):
        """
        Initializes the class

        The various input for the noise model is passed as
        parameters. Reasonable defaults are defined as well.
        'None' as input is converted to the corresponding default.

        @param image_name: the name of the input image
        @type image_name: string
        @param extname: the extension to use
        @type extname: string
        @param exptime: the exposure time
        @type exptime: float
        @param bck_flux: the background flux
        @type bck_flux: float or string
        @param qe: the quantum efficienty
        @type qe: float or string
        @param dc: the dark current
        @type dc: float or string
        @param rn: the readout noise
        @type rn: float or string
        @param cmap: path to cosmic map
        @type cmap: string
        @param reject: cosmic rejection
        @type reject: bool
        @param nbit: number of bits in raw image
        @type nbit: integer
        @param norm: normalize the final image
        @type norm: bool
        @param rdmode: read mode
        @type rdmode: string
        @param ngrp: number of group
        @type ngrp: integer
        @param nfrm: number of frame
        @type nfrm: integer
        @param dtgrp: time between each group
        @type dtgrp: float
        @param dtfrm: time between each frame
        @type dtfrm: float
        """
        # check whether the image exists
        if not os.path.isfile(image_name):
            err_msg = '\nImage: "'+image_name+'" does not exist!'
            raise aXeSIMError(err_msg)

        # save the parameters
        self.image_name = image_name
        self.extname    = extname
        self.exptime    = exptime
        self.detector   = detector
        self.norm = norm
        
        # determine and store the image dimensions
        self.dimension = self._get_dimension(self.image_name, self.extname)
        self.bck_flux = bck_flux
        self.qe = qe
        self.dc = dc
        self.rn    = rn

        if instrument != None:
            self.instrument = instrument
        else:
            self.instrument = 'aXeSIM'
        
        if cmap != 'None':
          self.cmap = cmap
        else:
          self.cmap = None

        self.reject = 'None'
        if reject != None and self.cmap != None:
          if reject == 'Perfect':
            self.reject = reject
          elif reject != 'None':
            print """
Error: value REJECT=%s unknown.
Value ignored.
            """ % reject
        
        self.nbit = None
        if nbit != None:
          try:
            self.nbit = int(nbit)
          except ValueError:
            print """
Error: NBIT=%s must be an integer.
Value ignored.
            """ % nbit
        
        self.rdmode = rdmode
        self.ngrp = ngrp
        self.nfrm = nfrm
        self.dtgrp = dtgrp
        self.dtfrm = dtfrm

    def _set_keywords(self, img):
        """
        Set header kewords in output image

        The method sets header keywords in the zero extension
        header of the output image.
        """

        img[0].header.update('INSTRUME', self.instrument, 'instrument name')
        img[0].header.update('EXPTIME', self.exptime, 'exposure time')
        img[self.extname].header.update('INSTRUME', self.instrument, 'instrument name')
        img[self.extname].header.update('EXTVER', 1)
        img[self.extname].header.update('GAIN', 1.0)
        if self.exptime != None:
            img[self.extname].header.update('EXPTIME', self.exptime, 'exposure time')
        if self.rn != None:
            img[self.extname].header.update('RDNOISE', self.rn)
        if self.qe != None:
            img[self.extname].header.update('QE', self.qe)
        if self.dc != None:
            img[self.extname].header.update('DC', self.dc)
        if self.cmap != None:
            img[self.extname].header.update('COSMAP', self.cmap)
            img[self.extname].header.update('REJECT', str(self.reject))
        if self.nbit != None:
            img[self.extname].header.update('NBIT', str(self.nbit))
        if self.rdmode != None:
            img[self.extname].header.update('RDMODE', str(self.rdmode))
        if self.ngrp != None:
            img[self.extname].header.update('NGRP', str(self.ngrp))
        if self.nfrm != None:
            img[self.extname].header.update('NFRM', str(self.nfrm))
        if self.dtgrp != None:
            img[self.extname].header.update('DTGRP', str(self.dtgrp))
        if self.dtfrm != None:
            img[self.extname].header.update('DTFRM', str(self.dtfrm))
        
    def _get_dimension(self, image_name, extname):
        """
        Get the image dimension

        @param image_name: the name of the image
        @type image_name: string
        @param extname: the extension name
        @type extname: string

        @return: the image-dimension (yaxis, xaxis)
        @rtype: (int, int)
        """
        import pyfits

        # open the fits
        f_img = pyfits.open(image_name, 'readonly')

        # extract the image dimension
        dimension = f_img[extname].data.shape

        # close the image
        f_img.close()

        # return the dimension
        return dimension

    def _load_noise(self, noise, shape):
        """
        Load noise 

        return the noise numpy array

        @param noise: noise
        @type noise: float or string
        """
        noisePath = None
        
        try:
                noise_value = float(noise)
                noise_flux = numpy.zeros(shape)+noise_value
        except ValueError:
                noisePath = putCONF(noise)
                if os.path.isfile(noisePath):
                        try:
                                noise_fits = pyfits.open(noisePath)
                                noise_flux = numpy.asarray(noise_fits[0].data)
                                if noise_flux.shape != shape:
                                        noise_flux = numpy.asarray(noise_fits[1].data)
                                        if noise_flux.shape != shape:
                                                print """
Error: noise shape not match.
Noise will set to zero.
                                                """
                                                noise_flux = numpy.zeros(shape)
                        except:
                                print """
Error: noise shape not match.
Noise will set to zero.
                                """
                                noise_flux = numpy.zeros(shape)

                else:
                        print """
Error: no such file %s.
Noise will set to zero.
                        """ % noisePath
                        noise_flux = numpy.zeros(shape)

        return (noise_flux, noisePath)

    def _add_regular_noise(self, flux_img, qe, dc, rn, cos):
        """
        This methid compute the noise using:
        * poisson statistic for signal
        * poisson statistic for the dark
        * gaussian statistic for the read noise.
        
        @param flux_img: simulated image of the sky flux [e-]
        @type flux_img: numpy array
        @param qe: array of quantum efficienty
        @type qe: numpy array
        @param dc: array of dark current in [e-]
        @type dc: numpy array
        @param rn: array of read noise in [e-]
        @type rn: numpy array
        @param cos: cosmics in [e-]
        @type cos: numpy array
        @return: tuple of the count image and the error image.
        """
        
        # compute counts
        count_img = (flux_img*qe)+dc+cos

        # compute errors
        err_img = (count_img+rn**2)**0.5

        # add fluctuations
        count_img[count_img>0] = stats.poisson.rvs(count_img[count_img>0])
        count_img = count_img + numpy.rint(numpy.random.normal(numpy.zeros(count_img.shape),rn))

        return (count_img, err_img)
        
    def _sim_detector(self, flux_img):
        """
        This method compute the number of counts for each pixel of the detector and the associated errors.
        
        @param flux_img: simulated image of the sky flux [e-]
        @type flux_img: numpy array
        @return: tuple of the science image, the error image end the mask image
        """
        
        print 'SIMDISPIM: Quantum Efficienty:            %s' % str(self.qe)
        print 'SIMDISPIM: Darck Current:                 %s' % str(self.dc)
        print 'SIMDISPIM: Read Noise:                    %s' % str(self.rn)
        
        # set mask array (same code than HST)
        dq_img = numpy.zeros(flux_img.shape, dtype=numpy.int)
        
        # load qe
        (qe,qe_path) = self._load_noise(self.qe, flux_img.shape)
        if qe_path !=None:
                self.qe = qe_path
        # flag bad pixel
        dq_img[(qe<0.0)&(dq_img<4)] = 4
        
        # load dc
        (dc,dc_path) = self._load_noise(self.dc, flux_img.shape)
        if dc_path!=None:
                self.dc = dc_path
        dc = dc*self.exptime
        # flag warm pixel
        dq_img[(dc>1000.0)&(dq_img<64)] = 64

        # load read noise
        (rn,rn_path) = self._load_noise(self.rn, flux_img.shape)
        if rn_path!=None:
                self.rn = rn_path
        # flag hot pixel
        dq_img[(rn>1000.0)&(dq_img<16)] = 16
        
        # load cosmic
        if self.cmap!=None:
                print 'SIMDISPIM: Cosmics:                       %s' % str(self.cmap)
                print 'SIMDISPIM: Reject:                        %s' % str(self.reject)
                (cos, cos_path) = self._load_noise(self.cmap, flux_img.shape)
                if cos_path!=None:
                        self.cmap = cos_path
                # flag cosmic
                dq_img[(cos>0)&(dq_img<8192)] = 8192
        else:
                cos = numpy.zeros(flux_img.shape)

        (count_img, err_img) = self._add_regular_noise(flux_img, qe, dc, rn, cos)
        
        # cosmic rejection
        if self.cmap!=None and self.reject == 'Perfect':
                sci_img = count_img - numpy.rint(cos)
        else:
                sci_img = count_img

        return (sci_img, err_img, dq_img)

    def _make_real_sciimage(self, signal):
        """
        Create the science extension

        Starting from a simulated image in [e/s], the module adds
        background and scales to [e]. The output image is returned.

        @param signal: image of the source flux in [e-/s]
        @type signal: numpy array
        @return: tuple of the science image, the error image end the mask image
        """

        print 'SIMDISPIM: Background flux/image:         %s' % str(self.bck_flux)

        # load background
        (bck_flux,bck_path) = self._load_noise(self.bck_flux, signal.shape)
        if bck_path!=None:
          self.bck_flux = bck_path
          
        # add background; scale by exptime
        flux_img = (signal+bck_flux)*self.exptime
        
        if not self.detector or self.rdmode == 'NoNoise':
                return (flux_img, flux_img**0.5, numpy.zeros(flux_img.shape, dtype=numpy.int))
        else:
                return self._sim_detector(flux_img)
        
    def make_real(self):
        """
        Create a 'natural' image

        Depending on the class data, method adds background and noise
        in ordr to create a 'natural' image from the plain,
        simulated image.
        """
        
        # load input image
        img = pyfits.open(self.image_name, mode='update')
        signal = numpy.asarray(img[self.extname].data)
        
        # set if needed exposure time
        if self.exptime == None or self.exptime == 0.0:
                self.exptime = 1.0
        print 'SIMDISPIM: Exposure time:                 %f' % self.exptime
        
        (sci,err,dq) = self._make_real_sciimage(signal)

        # numerical saturation
        if self.nbit != None and self.nbit>0:
                print 'SIMDISPIM: Number of bits:                %d' % self.nbit
                vsatnum = 2**self.nbit - 1
                sci[sci>vsatnum] = vsatnum
                dq[(sci>vsatnum)&(dq<256)] = 256
                if self.nbit <= 16:
                    sci = numpy.uint16(sci)
                elif self.nbit <= 32:
                    sci = numpy.uint32(sci)
                else:
                    sci = numpy.uint64(sci)
        
        # set header keyword
        self._set_keywords(img)

        print 'SIMDISPIM: Normalized:                    %s' % str(self.norm)
        if self.norm:
                sci = numpy.float64(sci) / self.exptime
                err = err / self.exptime
        
        # write output
        img[self.extname].data = sci
        img[len(img)-1].header.update('EXTVER', '1')
        img.append(pyfits.ImageHDU(err))
        img[len(img)-1].header.update('EXTNAME', 'ERR', 'name of this extension')
        img[len(img)-1].header.update('EXTVER', '1')
        img.append(pyfits.ImageHDU(dq))
        img[len(img)-1].header.update('EXTNAME', 'DQ', 'name of this extension')
        img[len(img)-1].header.update('EXTVER', '1')
        img.flush()
