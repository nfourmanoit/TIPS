"""
$Revision: 1.2 $ $Date: 2009/09/21 12:46:17 $
Author: Martin Kuemmel (mkuemmel@stecf.org)
Affiliation: Space Telescope - European Coordinating Facility
WWW: http://www.stecf.org/software/slitless_software/axesim/
"""
import os
import os.path
import sys
import string

import configfile

from axesimerror import *
from axesimutils import *
from inputchecker import *

class InputChecker(object):
    """
    Class to check task input

    This class is very close to static, the real beef is
    in the main methods. Hence the initialization method
    is rather naked.
    """
    def __init__(self):
        """
        Initializes the class
        """
        # just set the environments
        get_environments()

    def check_simdispim_input(self, incat, config, model_spectra, model_images, bck_flux):
        """
        Does basic checks on the parameters

        The method checks whether all input values are reasonable, e.g.
        the exposure time and background flux >= 0.0 and similar.
        Input files are checked for existence. Also the input type is
        checked for the numbers.

        @param incat: name of model object table
        @type incat: string
        @param config: aXe configuration file name
        @type config: string
        @param model_spectra: name of model spectra
        @type model_spectra: string
        @param model_images: name of model images
        @type model_image: string
        @param bck_flux: flux in background
        @type bck_flux: float
        """

        # check the existence of the
        # model object table
        if incat != None:
            if not os.path.isfile(putIMAGE(incat)):
                error_message = 'The Model Object Table does not exist: ' + putIMAGE(incat)
                raise aXeSIMError(error_message)

        # check the existence of the
        # axe configuration file
        if not os.path.isfile(putCONF(config)):
            error_message = 'The aXe configuration file does not exist: ' + putCONF(config)
            raise aXeSIMError(error_message)

        else:
            # load the aXe configuration file
            conf = configfile.ConfigFile(putCONF(config))

            # make the internal checks
            n_sens = conf.check_files()

            # make sure there is
            # at least one sens. file
            if n_sens < 1:
                error_message = 'There must be at least one sensitivity file in: ' + putCONF(config)
                raise aXeSIMError(error_message)

        if model_spectra != None:
            # check the existence of the
            # model spectra file
            if not os.path.isfile(putIMAGE(model_spectra)):
                error_message = 'The model spectra file does not exist: ' + putIMAGE(model_spectra)
                raise aXeSIMError(error_message)

        if model_images != None:
            # check the existence of the
            # model images file
            if not os.path.isfile(putIMAGE(model_images)):
                error_message = 'The model images file does not exist: ' + putIMAGE(model_images)
                raise aXeSIMError(error_message)

        try:
            # convert to float
            bck = float(bck_flux)

            # check for positive value
            if bck < 0:
                error_message = 'Value for "bck_flux" or "bck_flux_disp" most be positive: ' + str(bck_flux)
                raise aXeSIMError(error_message)

        # catch a string
        except ValueError:
            # check for existence of file
            if not os.path.isfile(putCONF(bck_flux)):
                error_message = 'The background file does not exist: ' + putCONF(bck_flux)
                raise aXeSIMError(error_message)


    def check_simdirim_input(self, incat, config, tpass_direct,
                             model_spectra, model_images,
                             nx, ny, exptime, bck_flux):
        """
        Does basic checks on the parameters

        The method checks whether all input values are reasonable, e.g.
        the exposure time and background flux >= 0.0 and similar.
        Input files are checked for existence. Also the input type is
        checked for the numbers.

        @param incat: name of model object table
        @type incat: string
        @param config: aXe configuration file name
        @type config: string
        @param tpass_direct: total passband file
        @type tpass_direct: string
        @param model_spectra: name of model spectra
        @type model_spectra: string
        @param model_images: name of model images
        @type model_image: string
        @param nx: number of pixels in x
        @type nx: int
        @param ny: number of pixels in y
        @type ny: int
        @param exptime: exposure time
        @type exptime: dloat
        @param bck_flux: flux in background
        @type bck_flux: dloat
        """
        # check the existence of the
        # model object table
        if not os.path.isfile(putIMAGE(incat)):
            error_message = 'The Model Object Table does not exist: ' + putIMAGE(incat)
            raise aXeSIMError(error_message)

        # check the existence of the
        # axe configuration file
        if not os.path.isfile(putCONF(config)):
            error_message = 'The aXe configuration file does not exist: ' + putCONF(config)
            raise aXeSIMError(error_message)

        else:
            # load the aXe configuration file
            conf = configfile.ConfigFile(putCONF(config))

            # make the internal checks
            n_sens = conf.check_files()

            # make sure there is
            # at least one sens. file
            if n_sens < 1:
                error_message = 'There must be at least one sensitivity file in: ' + putCONF(config)
                raise aXeSIMError(error_message)

        # check the existence of the
        # total passband file
        if not os.path.isfile(putSIMDATA(tpass_direct)):
            error_message = 'The total passband file does not exist: ' + putSIMDATA(tpass_direct)
            raise aXeSIMError(error_message)

        if model_spectra != None:
            # check the existence of the
            # model spectra file
            if not os.path.isfile(putIMAGE(model_spectra)):
                error_message = 'The model spectra file does not exist: ' + putIMAGE(model_spectra)
                raise aXeSIMError(error_message)

        if model_images != None:
            # check the existence of the
            # model images file
            if not os.path.isfile(putIMAGE(model_images)):
                error_message = 'The model images file does not exist: ' + putIMAGE(model_images)
                raise aXeSIMError(error_message)

        # check the nx-value
        if nx != None and nx <= 0.0:
            error_message = 'Value for "nx" or "nx_dir" most be positive: ' + str(nx)
            raise aXeSIMError(error_message)

        # check the ny-value
        if ny != None and ny <= 0:
            error_message = 'Value for "ny" or "ny_dir" most be positive: ' + str(ny)
            raise aXeSIMError(error_message)

        # check the exptime-value
        if exptime != None and exptime < 0:
            error_message = 'Value for "exptime" or "exptime_dir" most be positive: ' + str(exptime)
            raise aXeSIMError(error_message)

        if bck_flux != None:
            # check the bck_flux-value
            try:
                # convert to float
                bck = float(bck_flux)

                # check for positive value
                if bck < 0:
                    error_message = 'Value for "bck_flux" or "bck_flux_dir" most be positive: ' + str(bck_flux)
                    raise aXeSIMError(error_message)

                # catch a string
            except ValueError:
                # check for existence of file
                if not os.path.isfile(putCONF(bck_flux)):
                    error_message = 'The background file does not exist: ' + putCONF(bck_flux)
                    raise aXeSIMError(error_message)

