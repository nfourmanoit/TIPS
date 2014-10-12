"""
@author: Martin Kuemmel
@organization: LMU / USM
@license: Gnu Public Licence
@contact: mkuemmel@usm.lmu.de
@version:    $Revision: $
@date:       $Date: $
@changeDate: $LastChangedDate: $

Initialize the test library.
"""
import os.path
import shutil
import unittest

# check tips version
import tips
if float(tips.__version__)<2.0:
    vtipslt2 = True
else:
    vtipslt2 = False

class Test_AxesimDispBasic(unittest.TestCase):

    def setUp(self):
        # global detector-flag
        self.detectorFlag=True
        
        # global silent-flag
        self.silentFlag=True
        
        # the (list of) environment variables, names given to them and the files to be copied there
        subDirs = [('AXE_IMAGE_PATH', 'DATA', ['input_cat_test.spc.fits', 'input_cat_imgs.fits', 'input_stars_imgs.fits', 'HSTinput_cat_testI.dat', 'HSTinput_cat_testII.dat', 'HSTinput_cat_testIII.dat', 'HSTinput_cat_testIV.dat', 'HSTinput_cat_testV.dat', 'HSTinput_cat_testVI.dat']), \
                   ('AXE_CONFIG_PATH', 'CONF', ['Dummy.G141.V2.5.conf', 'Dummy.G141FF.V2.5.conf', 'WFC3.IR.G141.flat.2.fits', 'WFC3.IR.G141.1st.sens.2.fits', 'WFC3.IR.G141.0th.sens.1.fits', 'WFC3.IR.G141.2nd.sens.2.fits', 'WFC3.IR.G141.3rd.sens.2.fits', 'WFC3.IR.G141.m1st.sens.2.5.fits', 'mef_c4.00000_x-0.38167_y1.08146.fits']), \
                   ('AXE_OUTPUT_PATH', 'OUTPUT'), ('AXE_OUTSIM_PATH', 'OUTSIM'), \
                   ('AXE_SIMDATA_PATH', 'SIMDATA', ['wfc3_ir_f125w_tpass_m01.dat']), \
                   ('AXE_DRIZZLE_PATH', 'DRIZZLE')]

        # define the directory with the input data and make sure it exists
        self.dataDir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'HSTdata'))
        if not os.path.isdir(self.dataDir):
            errMsg = 'File does not exist: %s!' % self.dataDir
            raise Exception(errMsg)
        
        # define a name for the run directory;
        # destroy any old version;
        # create a new one
        #self.runDir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'verifyTests'))
        # run test in source directory may cause trouble depending where the code is integrated (not necessery writable)
        # new path is defined relative, assuming the test would be ran in a appropiate directory
        self.runDir = os.path.abspath('./axesimUnit')
        #if os.path.isdir(self.runDir):
        #    shutil.rmtree(self.runDir, ignore_errors=True, onerror=None)
        if not os.path.isdir(self.runDir):
            os.mkdir(self.runDir)

        # create the various sub-dirs
        # and point the environment variables on it
        for aSub in subDirs:
            subDir = os.path.join(self.runDir, aSub[1])
            if not os.path.isdir(subDir):
                os.mkdir(subDir)
            os.environ[aSub[0]] = subDir
            
            # copy files in this sub-dir
            if len(aSub) > 2:
                # extract the file list
                fileList = aSub[2]

                # copy files in the sub-dir
                for aFile in fileList:
                    # put together file names
                    inFile  = os.path.join(self.dataDir, aFile)
                    outFile = os.path.join(subDir, aFile)

                    # make sure the file exists
                    if not os.path.isfile(inFile):
                        errMsg = 'File does not exist: %s!' % self.dataDir
                        raise Exception(errMsg)

                    # copy the file
                    shutil.copy(inFile, outFile)

    """
    def tearDown(self):
        if os.path.isdir(self.runDir):
            shutil.rmtree(self.runDir, ignore_errors=True, onerror=None)
    """

    @unittest.skipIf(vtipslt2, "not supported in with tips < 2.0")
    def testGauss(self):
        """
        Only Gaussian objects
        """
        import axesim

        # make the simulation
        axesim.simdispim(incat='HSTinput_cat_testI.dat', config='Dummy.G141.V2.5.conf',
                         dispim_name='test_disp_Gauss.fits', exptime=200., bck_flux=0.5, 
                         detector=self.detectorFlag, silent=self.silentFlag)

        # check that the output image exists
        resultFile = os.path.join(os.environ['AXE_OUTSIM_PATH'], 'test_disp_Gauss.fits')
        self.assertTrue(os.path.isfile(resultFile), 'Output file does not exist: %s!' % resultFile)

    @unittest.skipIf(vtipslt2, "not supported in with tips < 2.0")
    def testGaussBB(self):
        """
        Gaussian objects with several broad band flux values
        """
        import axesim

        # make the simulation
        axesim.simdispim(incat='HSTinput_cat_testII.dat', config='Dummy.G141.V2.5.conf',
                         dispim_name='test_disp_Gauss_BB.fits', exptime=200., bck_flux=0.5, 
                         detector=self.detectorFlag, silent=self.silentFlag)

        # check that the output image exists
        resultFile = os.path.join(os.environ['AXE_OUTSIM_PATH'], 'test_disp_Gauss_BB.fits')
        self.assertTrue(os.path.isfile(resultFile), 'Output file does not exist: %s!' % resultFile)

    @unittest.skipIf(vtipslt2, "not supported in with tips < 2.0")
    def testModImgBB(self):
        """
        Model images with several broad band flux values
        """
        import axesim

        # make the simulation
        axesim.simdispim(incat='HSTinput_cat_testIII.dat', config='Dummy.G141.V2.5.conf',
                         dispim_name='test_disp_modimg_BB.fits', model_images='input_cat_imgs.fits',
                         exptime=200., bck_flux=0.5, detector=self.detectorFlag, silent=self.silentFlag)

        # check that the output image exists
        resultFile = os.path.join(os.environ['AXE_OUTSIM_PATH'], 'test_disp_modimg_BB.fits')
        self.assertTrue(os.path.isfile(resultFile), 'Output file does not exist: %s!' % resultFile)

    @unittest.skipIf(vtipslt2, "not supported in with tips < 2.0")
    def testModImgSpec(self):
        """
        Model images with input spectra
        """
        import axesim

        # make the simulation
        axesim.simdispim(incat='HSTinput_cat_testIV.dat', config='Dummy.G141.V2.5.conf',
                         dispim_name='test_disp_modimg_spec.fits', model_images='input_cat_imgs.fits', model_spectra='input_cat_test.spc.fits',
                         exptime=200., bck_flux=0.5, detector=self.detectorFlag, silent=self.silentFlag)

        # check that the output image exists
        resultFile = os.path.join(os.environ['AXE_OUTSIM_PATH'], 'test_disp_modimg_spec.fits')
        self.assertTrue(os.path.isfile(resultFile), 'Output file does not exist: %s!' % resultFile)

    @unittest.skipIf(vtipslt2, "not supported in with tips < 2.0")
    def testMixed(self):
        """
        With/without model images, with/without spectra
        """
        import axesim

        # make the simulation
        axesim.simdispim(incat='HSTinput_cat_testV.dat', config='Dummy.G141.V2.5.conf',
                         dispim_name='test_disp_mixed.fits', model_images='input_cat_imgs.fits', model_spectra='input_cat_test.spc.fits',
                         exptime=200., bck_flux=0.5, detector=self.detectorFlag, silent=self.silentFlag)

        # check that the output image exists
        resultFile = os.path.join(os.environ['AXE_OUTSIM_PATH'], 'test_disp_mixed.fits')
        self.assertTrue(os.path.isfile(resultFile), 'Output file does not exist: %s!' % resultFile)

    @unittest.skipIf(vtipslt2, "not supported in with tips < 2.0")
    def testMixedwPSF(self):
        """
        With/without model images, with/without spectra, PSF convolution
        """
        import axesim

        # make the simulation
        axesim.simdispim(incat='HSTinput_cat_testV.dat', config='Dummy.G141.V2.5.conf',
                         dispim_name='test_disp_mixed_psf.fits', model_images='input_cat_imgs.fits', model_spectra='input_cat_test.spc.fits',
                         psf_file='mef_c4.00000_x-0.38167_y1.08146.fits', exptime=200., bck_flux=0.5, detector=self.detectorFlag, silent=self.silentFlag)

        # check that the output image exists
        resultFile = os.path.join(os.environ['AXE_OUTSIM_PATH'], 'test_disp_mixed_psf.fits')
        self.assertTrue(os.path.isfile(resultFile), 'Output file does not exist: %s!' % resultFile)

    @unittest.skipIf(vtipslt2, "not supported in with tips < 2.0")
    def testMixedwPSFwFF(self):
        """
        With/without model images, with/without spectra, PSF convolution and inverse flat-field
        """
        import axesim

        # make the simulation
        axesim.simdispim(incat='HSTinput_cat_testV.dat', config='Dummy.G141FF.V2.5.conf',
                         dispim_name='test_disp_mixed_psf_ff.fits', model_images='input_cat_imgs.fits', model_spectra='input_cat_test.spc.fits',
                         psf_file='mef_c4.00000_x-0.38167_y1.08146.fits', exptime=200., bck_flux=0.5, detector=self.detectorFlag, silent=self.silentFlag)

        # check that the output image exists
        resultFile = os.path.join(os.environ['AXE_OUTSIM_PATH'], 'test_disp_mixed_psf_ff.fits')
        self.assertTrue(os.path.isfile(resultFile), 'Output file does not exist: %s!' % resultFile)

    @unittest.skipIf(vtipslt2, "not supported in with tips < 2.0")
    def testMixedStars(self):
        """
        'Stellar' sources as model images
        """
        import axesim

        # make the simulation
        axesim.simdispim(incat='HSTinput_cat_testVI.dat', config='Dummy.G141FF.V2.5.conf',
                         dispim_name='test_disp_stars.fits', model_images='input_stars_imgs.fits', model_spectra='input_cat_test.spc.fits',
                         psf_file='mef_c4.00000_x-0.38167_y1.08146.fits', exptime=200., bck_flux=0.5, detector=self.detectorFlag, silent=self.silentFlag)

        # check that the output image exists
        resultFile = os.path.join(os.environ['AXE_OUTSIM_PATH'], 'test_disp_stars.fits')
        self.assertTrue(os.path.isfile(resultFile), 'Output file does not exist: %s!' % resultFile)

