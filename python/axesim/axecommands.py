"""
$Revision: 1.2 $ $Date: 2009/09/21 12:46:17 $
Author: Martin Kuemmel (mkuemmel@stecf.org)
Affiliation: Space Telescope - European Coordinating Facility
WWW: http://www.stecf.org/software/slitless_software/axesim/
Modified by Julien Zoubian
"""
import os
import os.path
import sys
import subprocess

from axesimerror import *
from axesimutils import *

# define the good return
# value for the binaries
GOOD_RETURN_VALUE = 0

class TaskWrapper(object):
    """
    General class to execute C-tasks
    """
    def __init__(self, taskname, tshort):
        """
        Initializer for the class

        @param taskname: name of the C-executable
        @type taskname: string
        @param tshort: shor name for task
        @type tshort: string
        """
        self.taskname = taskname
        self.tshort   = tshort

        # initialize the command list
        self.command_list = []

        # save a name for stdout
        self.stdout = putOUTPUT(get_random_filename(tshort, '.stdout'))

        # save a name for stderr
        self.stderr = putOUTPUT(get_random_filename(tshort, '.stderr'))

        # put the command into the list
        self.command_list.append(putAXESIMBIN(taskname))

    def run(self, silent=False):
        """
        Run the wrapped task

        The method executes the associated C-executable. The return code given
        by the C-executable is returned. In silent mode stdout and stderr
        are writtren to a file, in non-silent mode to the screen.

        @param silent: boolean for silent mode
        @type silent: boolean

        @return: the return code of the C-executable
        @rtype: int
        """
        # is output desired
        if silent:
            # open stdout/stderr
            sout = open(self.stdout, 'w+')
            serr = open(self.stderr, 'w+')

            # execute the task
            sout.write(str(self.command_list))
            sout.flush()
            retcode = subprocess.call(self.command_list, stdout=sout, stderr=serr)

            # close stdout/stderr
            sout.close()
            serr.close()

        else:

            # execute the task with the default stdout and
            # stderr, which is the system one
            retcode = subprocess.call(self.command_list)

        # return the result
        return retcode

    def cleanup(self):
        """
        Clean up some mess

        The method deletes the files created for stdout and stderr.
        This is a usual cleaning procedure in case nothing bad happened.
        """
        # delete stdout/stderr
        if os.path.isfile(self.stdout):
            os.unlink(self.stdout)
        if os.path.isfile(self.stderr):
            os.unlink(self.stderr)

    def print_outputs(self):
        """
        Print all output

        The method prints the files collected from the
        standard out and standard error of the C-task
        to the standard output.
        For debugging.
        """
        # print the stdout file
        for aLine in file(self.stdout).readlines():
            print aLine.strip()

        # print the stderr file
        for aLine in file(self.stderr).readlines():
            print aLine.strip()

    def report_all(self, silent=True):
        """
        Print stdout and stderr on the screen

        The method gives a feedback in case of problems. stdout and stderr
        are both listed onto the screen for a further interactive analysis.

        @param silent: indicates silent/noisy runs
        @type silent: boolean
        """
        # check whether the command
        # was run silent
        if silent:
            # dump the files with
            # stdout and stderr onto the screen
            print '\nThere was a problem in the task: ', self.taskname
            print 'The output of the task (file "' + self.stdout + ')" is:'
            print '--------------------------------------------------------------------------------'
            for line in open(self.stdout):
                print string.strip(line)
            print '\n\nThe error report is of the task (file "' + self.stdout +'") is:'
            print '--------------------------------------------------------------------------------'
            for line in open(self.stderr):
                print string.strip(line)

        # report an error
        raise aXeSIMError('An error occured in the aXe task: ' + self.taskname)

class aXe_SEX2GOL(TaskWrapper):
    """
    Wrapper around the aXe_SEX2GOL task
    """
    def __init__(self, grismname, configfile, iolname, dirname=None):
        """
        Initializer for the class

        This method is a simple initializer for the class. All
        variables a transferred to a list, if necessary with the
        appropriate leading parameter name

        @param grismname: name of the dispersed image
        @type grismname: string
        @param configfile: name of the aXe configuration file
        @type configfile: string
        @param iolname: name of the input object list
        @type iolname: string
        @param dirname: name of the direct image
        @type dirname: string
        """
        # initialize via superclass
        super(aXe_SEX2GOL, self).__init__('aXe_SEX2GOL', 'sex2gol')

        # check whether a direct image exists
        if dirname != None:
            # put the direct image name to the list
            self.command_list.append(dirname)

            # put the grism name to the list
            self.command_list.append(grismname)

            # put the grism name to the list
            self.command_list.append(configfile)
        else:
            # put the grism name to the list
            self.command_list.append(grismname)

            # put the grism name to the list
            self.command_list.append(configfile)

            # mark that there is no direct image
            self.command_list.append('-no_direct_image')

        # put the grism name to the list
        self.command_list.append('-in_SEX='+iolname)


class aXe_GOL2AF(TaskWrapper):
    """
    Wrapper around the aXe_GOL2AF task
    """
    def __init__(self, grismname, configfile, extrfwhm=None, orient=0,
                 slitless_geom=0, lambda_mark=None):
        """
        Initializer for the class

        This method is a simple initializer for the class. All
        variables a transferred to a list, if necessary with the
        appropriate leading parameter name

        @param grismname: name of the dispersed image
        @type grismname: string
        @param configfile: name of the aXe configuration file
        @type configfile: string
        @param mfwhm: extraction width
        @type mfwhm: float
        @param orient: orient flag
        @type orient: int
        @param lambda_mark: lambda-mark value
        @type lambda_mark: float
        """
        # initialize via superclass
        super(aXe_GOL2AF, self).__init__('aXe_GOL2AF', 'gol2af')

        # put the grism name to the list
        self.command_list.append(grismname)

        # put the grism name to the list
        self.command_list.append(configfile)

        if extrfwhm != None:
            # put the fwhm to the list
            self.command_list.append('-mfwhm='+str(extrfwhm))

        if orient:
            # put the orient flag to the list
            self.command_list.append('-orient=1')
        else:
            self.command_list.append('-orient=0')
            # put the auto-orient flag to the list
            self.command_list.append('-orient='+str(orient))

        if slitless_geom:
            # put the slitless=-optimize flag to the list
            self.command_list.append('-slitless_geom=1')
        else:
            self.command_list.append('-slitless_geom=0')

        if lambda_mark != None:
            # put the lambda_mark value to the list
            self.command_list.append('-lambda_mark='+str(lambda_mark))


class aXe_AF2PET(TaskWrapper):
    """
    Wrapper around the aXe_AF2PET task
    """
    def __init__(self, grismname, configfile):
        """
        Initializer for the class

        This method is a simple initializer for the class. All
        variables a transferred to a list, if necessary with the
        appropriate leading parameter name

        @param grismname: name of the dispersed image
        @type grismname: string
        @param configfile: name of the aXe configuration file
        @type configfile: string
        """
        # initialize via superclass
        super(aXe_AF2PET, self).__init__('aXe_AF2PET', 'af2pet')

        # put the grism name to the list
        self.command_list.append(grismname)

        # put the grism name to the list
        self.command_list.append(configfile)


class aXe_PET2SPC(TaskWrapper):
    """
    Wrapper around the aXe_PET2SPC task
    """
    def __init__(self, grismname, configfile, smooth_conv=True, bpet=0):
        """
        Initializer for the class

        This method is a simple initializer for the class. All
        variables a transferred to a list, if necessary with the
        appropriate leading parameter name

        @param grismname: name of the dispersed image
        @type grismname: string
        @param configfile: name of the aXe configuration file
        @type configfile: string
        @param bpet: marks the existence of a background pet
        @type bpet: int
        """
        # initialize via superclass
        super(aXe_PET2SPC, self).__init__('aXe_PET2SPC', 'pet2spc')

        # put the grism name to the list
        self.command_list.append(grismname)

        # put the grism name to the list
        self.command_list.append(configfile)

        # add the no-bpet flagg
        if not bpet:
            self.command_list.append('-noBPET')

        # add the flag for smooth
        # sensitivity conversion
        if smooth_conv:
            self.command_list.append('-smooth_conv')

class aXe_STAMPS(TaskWrapper):
    """
    Wrapper around the aXe_STAMPS task
    """
    def __init__(self, grismname, configfile, rectified=1):
        """
        Initializer for the class

        This method is a simple initializer for the class. All
        variables a transferred to a list, if necessary with the
        appropriate leading parameter name

        @param grismname: name of the dispersed image
        @type grismname: string
        @param configfile: name of the aXe configuration file
        @type configfile: string
        @param rectified: flagg for rectified stamps
        @type rectified: int
        """
        # initialize via superclass
        super(aXe_STAMPS, self).__init__('aXe_STAMPS', 'stamps')

        # put the grism name to the list
        self.command_list.append(grismname)

        # put the grism name to the list
        self.command_list.append(configfile)

        # add the rectified flagg
        if rectified:
            self.command_list.append('-rectified')


class aXe_PETCONT(TaskWrapper):
    """
    Wrapper around the aXe_PETCONT task
    """
    def __init__(self, grismname, configfile, lambda_psf=None,
                 model_spectra=None, model_images=None):
        """
        Initializer for the class

        This method is a simple initializer for the class. All
        variables a transferred to a list, if necessary with the
        appropriate leading parameter name

        @param grismname: name of the dispersed image
        @type grismname: string
        @param configfile: name of the aXe configuration file
        @type configfile: string
        @param lambda_psf: reference wavelength for the psf
        @type lambda_psf: float
        @param model_spectra: name of the model spectra file
        @type model_spectra: string
        @param model_images: name of the model image file
        @type model_images: string
        """
        # initialize via superclass
        super(aXe_PETCONT, self).__init__('aXe_PETCONT', 'petcont')

        # put the grism name to the list
        self.command_list.append(grismname)

        # put the aXe configuration file name to the list
        self.command_list.append(configfile)

        # put the contamination map flagg
        self.command_list.append('-cont_map')

        # check whether the wavelength for the psf determination
        # was given, append the number to the list
        if lambda_psf != None:
            self.command_list.append('-lambda_psf='+str(lambda_psf))

        # check whether model spectra are given
        # append the file name to the list
        if model_spectra != None:
            self.command_list.append('-model_spectra='+str(model_spectra))

        # check whether model images are given
        # append the file name to the list
        if model_images != None:
            self.command_list.append('-model_images='+str(model_images))
            self.command_list.append('-cont_model=2')
        else:
            self.command_list.append('-cont_model=1')

        # append the no-PET flagg
        self.command_list.append('-noPET')

        # append the no-PET flagg
        self.command_list.append('-model_scale=5')

class aXe_DIRIMAGE(TaskWrapper):
    """
    Wrapper around the aXe_DIRIMAGE task
    """
    def __init__(self, dirname, configfile, tpass_direct, model_spectra=None,
                 model_images=None, tel_area=None):
        """
        Initializer for the class

        This method is a simple initializer for the class. All
        variables a transferred to a list, if necessary with the
        appropriate leading parameter name

        @param dirname: name of the direct image
        @type dirname: string
        @param configfile: name of the aXe configuration file
        @type configfile: string
        @param tpass_direct: name of the total passband file
        @type tpass_direct: string
        @param model_spectra: name of the model spectra file
        @type model_spectra: string
        @param model_images: name of the model image file
        @type model_images: string
        @param tel_area: collecting area of the telescope
        @type tel_area: float
        """
        # initialize via superclass
        super(aXe_DIRIMAGE, self).__init__('aXe_DIRIMAGE', 'dirimage')

        # put the direct image name to the list
        self.command_list.append(dirname)

        # put the aXe configuration file name to the list
        self.command_list.append(configfile)

        # put the total passband file name to the list
        self.command_list.append(tpass_direct)

        # check whether model spectra are given
        # append the file name to the list
        if model_spectra != None:
            self.command_list.append('-model_spectra='+str(model_spectra))

        # check whether model images are given
        # append the file name to the list
        if model_images != None:
            self.command_list.append('-model_images='+str(model_images))

        # check whether model images are given
        # append the file name to the list
        if tel_area != None:
            self.command_list.append('-tel_area='+str(tel_area))

        # append the no-PET flagg
        self.command_list.append('-model_scale=5')

class aXe_DISPIMAGE(TaskWrapper):
    """
    Wrapper around the aXe_PETCONT task
    """
    def __init__(self, grismname, configfile, lambda_psf=None,
                 model_spectra=None, model_images=None):
        """
        Initializer for the class

        This method is a simple initializer for the class. All
        variables a transferred to a list, if necessary with the
        appropriate leading parameter name

        @param grismname: name of the dispersed image
        @type grismname: string
        @param configfile: name of the aXe configuration file
        @type configfile: string
        @param lambda_psf: reference wavelength for the psf
        @type lambda_psf: float
        @param model_spectra: name of the model spectra file
        @type model_spectra: string
        @param model_images: name of the model image file
        @type model_images: string
        """
        # initialize via superclass
        super(aXe_DISPIMAGE, self).__init__('aXe_DISPIMAGE', 'dispimage')

        # put the grism name to the list
        self.command_list.append(grismname)

        # put the aXe configuration file name to the list
        self.command_list.append(configfile)

        # check whether the wavelength for the psf determination
        # was given, append the number to the list
        if lambda_psf != None:
            self.command_list.append('-lambda_psf='+str(lambda_psf))

        # check whether model spectra are given
        # append the file name to the list
        if model_spectra != None:
            self.command_list.append('-model_spectra='+str(model_spectra))

        # check whether model images are given
        # append the file name to the list
        if model_images != None:
            self.command_list.append('-model_images='+str(model_images))

class DispImator(object):
    """
    Class to create a dispersed image
    """
    def __init__(self, dummyImages, configfile, simobjects, lambda_psf=None,
                 model_spectra=None, model_images=None):
        """
        Initializer for the class

        @param dummyImages: dummy image structure
        @type dummyImages: DummyImages()
        @param configfile: name of the aXe configuration file
        @type configfile: string
        @param simobjects: name of the model object table
        @type simobjects: string
        @param lambda_psf: reference wavelength for the psf
        @type lambda_psf: float
        @param model_spectra: name of the model spectra file
        @type model_spectra: string
        @param model_images: name of the model image file
        @type model_images: string
        """
        # save the naked name of the grism image
        self.grismname  = os.path.basename(dummyImages.griname)

        # check whether there is a direct image
        if dummyImages.dirname != None:
            # save the direct image name
            self.dirname = os.path.basename(dummyImages.dirname)
        else:
            # set the direct image name to 'None'
            self.dirname = None

        # save all other input to class variables
        self.configfile    = configfile
        self.iolname       = simobjects
        self.model_spectra = model_spectra
        self.model_images  = model_images
        self.lambda_psf    = lambda_psf

    def run(self, silent=True):
        """
        Generates a simulated dispersed image

        The method executes the series of aXe tasks necessary to generate
        a simulated dispersed image. The input from the class data is
        supplemented with default values.

        @param silent: boolean for silent mode
        @type silent: boolean
        """
        # define and run SEX2GOL
        sex2gol = aXe_SEX2GOL(self.grismname, self.configfile, self.iolname, self.dirname)
        print 'Running task "sex2gol" ...',
        sys.stdout.flush()
        retcode = sex2gol.run(silent=silent)
        print ' Done'
        if retcode == GOOD_RETURN_VALUE:
            sex2gol.cleanup()
        else:
            sex2gol.report_all(silent)
            error_message = 'Error in task: ' + 'sex2gol!'
            raise aXeSIMError(error_message)

        # define and run GOL2AF
        gol2af = aXe_GOL2AF(self.grismname, self.configfile, orient=1, slitless_geom=1)
        print 'Running task "gol2af" ...',
        sys.stdout.flush()
        retcode = gol2af.run(silent=silent)
        print ' Done'
        if retcode == GOOD_RETURN_VALUE:
            gol2af.cleanup()
        else:
            gol2af.report_all(silent)
            error_message = 'Error in task: ' + 'gol2af!'
            raise aXeSIMError(error_message)

        # define and run DISPIMAGE
        dispimage = aXe_DISPIMAGE(self.grismname, self.configfile, lambda_psf=self.lambda_psf,
                              model_spectra=self.model_spectra, model_images=self.model_images)
        
        print 'Running task "dispimage" ...',
        sys.stdout.flush()
        retcode = dispimage.run(silent=silent)
        print ' Done'
        if retcode == GOOD_RETURN_VALUE:
            dispimage.cleanup()
        else:
            dispimage.report_all(silent)
            error_message = 'Error in task: ' + 'dispimage!'
            raise aXeSIMError(error_message)

    def mopup(self):
        """
        Deleting GOL and OAF files
        """
        import shutil

        # get the root name of the dispersed image
        pos = self.grismname.rfind('.fits')
        root_name   = self.grismname[:pos]

        # delete the GOL, the OAF 
        result_cat = putOUTPUT(root_name   + '_2.cat')
        if os.path.isfile(result_cat):
            os.unlink(result_cat)
        result_oaf = putOUTPUT(root_name   + '_2.OAF')
        if os.path.isfile(result_oaf):
            os.unlink(result_oaf)

class DirImator(object):
    """
    Class to create a direct image
    """
    def __init__(self, dummyImages, configfile, simobjects, tpass_direct,
                 model_spectra=None, model_images=None, tel_area=None):
        """
        Initializer for the class

        @param dummyImages: dummy image structure
        @type dummyImages: DummyImages()
        @param configfile: name of the aXe configuration file
        @type configfile: string
        @param simobjects: name of the model object table
        @type simobjects: string
        @param tpass_direct: name of the total passband file
        @type tpass_direct: string
        @param model_spectra: name of the model spectra file
        @type model_spectra: string
        @param model_images: name of the model image file
        @type model_images: string
        @param tel_area: the collecting area of the telescope
        @type tel_area: float
        """
        # save the naked name of the direct image
        self.dirname = os.path.basename(dummyImages.dirname)

        # save all other input to local variables
        self.configfile    = configfile
        self.iolname       = simobjects
        self.tpass_direct  = tpass_direct
        self.model_spectra = model_spectra
        self.model_images  = model_images
        self.tel_area      = tel_area


    def run(self, silent=True):
        """
        Generates a simulated direct image

        The method executes the series of aXe tasks necessary to generate
        a simulated direct image.

        @param silent: boolean for silent mode
        @type silent: boolean
        """
        # define and run SEX2GOL
        sex2gol = aXe_SEX2GOL(self.dirname, self.configfile, self.iolname)
        print 'Running task "sex2gol" ...',
        sys.stdout.flush()
        retcode = sex2gol.run(silent=silent)
        print ' Done'
        if retcode == GOOD_RETURN_VALUE:
            sex2gol.cleanup()
        else:
            sex2gol.report_all(silent)

        # define and run GOL2AF
        gol2af = aXe_GOL2AF(self.dirname, self.configfile)
        print 'Running task "gol2af" ...',
        sys.stdout.flush()
        retcode = gol2af.run(silent=silent)
        print ' Done'
        if retcode == GOOD_RETURN_VALUE:
            gol2af.cleanup()
        else:
            gol2af.report_all(silent)

        # define and run DIRIMAGE
        dirimage = aXe_DIRIMAGE(self.dirname, self.configfile, self.tpass_direct,
                                model_spectra=self.model_spectra, model_images=self.model_images,
                                tel_area=self.tel_area)

        print 'Running task "dirimage" ...',
        sys.stdout.flush()
        retcode = dirimage.run(silent=silent)
        print ' Done'
        if retcode == GOOD_RETURN_VALUE:
            dirimage.cleanup()
        else:
            dirimage.report_all(silent)

    def mopup(self):
        """
        Deleting GOL and OAF files
        """
        import shutil

        # get the root name of the dispersed image
        pos = self.dirname.rfind('.fits')
        root_name   = self.dirname[:pos]

        # delete the GOL, the OAF and the PET
        result_cat = putOUTPUT(root_name   + '_2.cat')
        if os.path.isfile(result_cat):
            os.unlink(result_cat)
        result_oaf = putOUTPUT(root_name   + '_2.OAF')
        if os.path.isfile(result_oaf):
            os.unlink(result_oaf)



