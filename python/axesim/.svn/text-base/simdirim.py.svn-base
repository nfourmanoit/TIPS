"""
$Revision: 1.1 $ $Date: 2008/09/05 08:01:40 $
Author: Martin Kuemmel (mkuemmel@stecf.org)
Affiliation: Space Telescope - European Coordinating Facility
WWW: http://www.stecf.org/software/slitless_software/axesim/
"""
import shutil

import imagemaker
import interpolator
import modspeclist
import axecommands
import realworld
import configfile

from axesimerror  import *
from axesimutils  import *
from inputchecker import *

def simdirim(incat=None, config=None, tpass_direct=None, dirim_name=None,
             model_spectra=None, model_images=None, nx=None, ny=None,
             exptime=None, bck_flux=0.0, silent=True, detector=True, norm=True):
    """
    Main function for the task SIMDIRIM

    This module is the high level wrapper function for the
    task SIMDIRIM. All necessary actions are done, feedback
    is given to the user

    @param incat: name of model object table
    @type incat: string
    @param config: aXe configuration file name
    @type config: string
    @param tpass_direct: total passband file
    @type tpass_direct: string
    @param dirim_name: name of direct image
    @type dirim_name: string
    @param model_spectra: name of model spectra file
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
    @type bck_flux: float
    @param silent: flag for silent run
    @type silen: boolean
    """
    # give brief feedback
    print '\nSIMDIRIM: Starting ...'

    # just set the environments
    get_environments()

    if incat == None or  config==None or tpass_direct==None:
        print __doc__
        return 1


    # check the input parameters
    in_check = InputChecker()
    # for the 'simdisp'-task
    in_check.check_simdirim_input(incat, config, tpass_direct,
                                  model_spectra, model_images, nx,
                                  ny, exptime, bck_flux)

    if dirim_name == None:
        # derive the output name
        pos = incat.rfind('.')
        if pos < 0:
            dirima_name  = incat + '_direct.fits'
        else:
            dirima_name  = incat[:pos] + '_direct.fits'
    else:
        dirima_name  = dirim_name

    # make a full path to the
    # direct image as dummy and as final output
    dummy_dirima_path = putIMAGE(dirima_name)
    final_dirima_path = putOUTSIM(dirima_name)

    try:
        # to convert the background value
        # to a float
        bck_flux = float(bck_flux)
    except ValueError:
        # now it must be a file;
        # check for its existence
        if not os.path.isfile(putCONF(bck_flux)):
            err_msg = 'Missing background image: ' + putCONF(bck_flux)
            raise aXeSIMError(err_msg)

        # store the path to the
        # background image
        bck_flux = putCONF(bck_flux)


    # load the aXe configuration file
    conf = configfile.ConfigFile(putCONF(config))

    # make the simulation configuration
    # file pointing the correct extensions
    config_simul = conf.axesim_prep()
   
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

    # delete the object
    # explicitly
    del conf

    # load the simulation configuration file
    conf_simul = configfile.ConfigFile(putCONF(config_simul))
 
    print 'SIMDIRIM: Input Model Object List:       %s' % putIMAGE(incat)
    print 'SIMDIRIM: Input aXe configuration file:  %s' % putCONF(config)
    print 'SIMDIRIM: Input Total Passband file:     %s' % putSIMDATA(tpass_direct)
    if model_spectra != None:
        print 'SIMDIRIM: Input Model Spectra:           %s' % putIMAGE(model_spectra)
    if model_images != None:
        print 'SIMDIRIM: Input Model Spectra:           %s' % putIMAGE(model_images)
    print 'SIMDIRIM: Background flux/image:         %s' % str(bck_flux)
    if exptime != None:
        print 'SIMDIRIM: Input exposure time:           %s' % str(exptime)
    if nx == None and ny == None:
        print 'SIMDIRIM: Input image dimensions:        %s' % 'AUTO'
    else:
        print 'SIMDIRIM: Input image dimensions:        (%s,%s)' % (str(nx),str(ny))

    print 'SIMDIRIM: Output dispersed image:        %s' % final_dirima_path
    print ''

    # check whether the name ends with '.fits'
    if not tpass_direct.rfind('.fits') == len(tpass_direct)-len('.fits'):

        # load the ascii list
        new_interp = interpolator.Interpolator(putSIMDATA(tpass_direct))

        # save it as fits
        new_name = new_interp.writetofits(colname1='WAVELENGTH', colname2='THROUGHPUT')

        # give feedback
        print 'Ascii list: ', tpass_direct, ' converted to fits: ', new_name

        # overwrite the old name
        tpass_direct = os.path.basename(new_name)

    # create the dummy image maker
    i_maker = imagemaker.DummyImages(putCONF(config_simul), dirname=dummy_dirima_path,
                                     nx=nx, ny=ny)
    # nake the dummy images
    i_maker.makeImages()

    # load the model object table
    inobjects = modspeclist.ModelObjectTable(putIMAGE(incat))
    # fill the model object table
    inobjects.fill_columns(i_maker.WCSimage, i_maker.WCSext)

    # load the object to make the grism simulations
    dirmator = axecommands.DirImator(i_maker, config_simul, putIMAGE(incat), tpass_direct,
                                     model_spectra, model_images, float(conf_simul['TELAREA']))
    dirmator.run(silent=silent)
    dirmator.mopup()

    # delete the dummy images
    i_maker.deleteImages()

    # get the name of the result image, which is the contamination image
    result_image = putOUTPUT(dirima_name.replace('.fits','_2.CONT.fits'))

    # convert the 'contamination' image into
    # a full output image with three extensions
    # and noise (if desired)
    rworld = realworld.RealWorld(result_image, extname='SCI', exptime=exptime,
                                 bck_flux=bck_flux, qe=conf_simul['QE'], dc=conf_simul['DC'], rn=conf_simul['RDNOISE'],
                                 instrument=conf_simul['INSTRUMENT'], detector=detector, cmap=conf_simul['COSMAP'],
                                 reject=conf_simul['REJECT'], nbit=conf_simul['NBIT'], norm=norm, rdmode=conf_simul['RDMODE'], 
                                 ngrp=conf_simul['NGRP'], nfrm=conf_simul['NFRM'], dtgrp=conf_simul['DTGRP'], dtfrm=conf_simul['DTFRM'])
    rworld.make_real()

    # move the resulting image to the correct
    # name and place
    shutil.move(result_image, final_dirima_path)

    # give brief feedback
    print 'SIMDIRIM: Done ...\n'
    return 0


"""
def main():
    # just set the environments
    get_environments()

    if len(sys.argv) < 3:
        print __doc__
        sys.exit(1)

    elif len(sys.argv) < 4:
        incat = sys.argv[1]
        config = sys.argv[2]
        nx = None
        ny = None
        # derive the output name
        pos = incat.rfind('.')
        if pos < 0:
            dirima_name  = putIMAGE(incat + '_direct.fits')
            grisima_name = putIMAGE(incat + '_slitless.fits')
        else:
            dirima_name  = putIMAGE(incat[:pos] + '_direct.fits')
            grisima_name = putIMAGE(incat[:pos] + '_slitless.fits')
    else:
        incat = sys.argv[1]
        config = sys.argv[2]
        nx = None
        ny = None
        grisim_name = sys.argv[3]
        dirima_name  = putIMAGE(grisim_name + '_direct.fits')
        grisima_name = putIMAGE(grisim_name + '_slitless.fits')

    # load the aXe configuration file
    conf = configfile.ConfigFile(putCONF(config))
    # make sure it points to the
    # right science extension
    conf.axesim_prep()

    # create the dummy image maker
    i_maker = imagemaker.DummyImages(putCONF(config), grisima_name,
                                     dirima_name, nx, ny)
    # nake the dummy images
    i_maker.makeImages()

    # load the model object table
    inobjects = modspeclist.ModelObjectTable(putIMAGE(incat))
    # fill the model object table
    inobjects.fill_columns(i_maker.WCSimage, i_maker.WCSext)

    # delete the dummy images
    #i_maker.deleteImages()

    axax = axecommands.aXiator(i_maker, config, putIMAGE(incat))
    axax.run()

    # delete the dummy images
    #i_maker.deleteImages()

if __name__ == '__main__':
    # go for the main
    main()
"""
