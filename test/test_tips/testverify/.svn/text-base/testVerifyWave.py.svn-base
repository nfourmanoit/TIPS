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

class Test_VerifyWaveBasic(unittest.TestCase):

    def setUp(self):
        # flag for mop up
        self.doRemove = False

        # global detector-flag
        self.detectorFlag=False
        
        # global silent-flag
        self.silentFlag=True
        
        # the (list of) environment variables, names given to them and the files to be copied there
        subDirs = [('AXE_IMAGE_PATH', 'DATA', ['galaxyThumbs.fits', 'input_stars_imgs.fits', 'input_line.spc.fits', 'input_cat_verifyI.dat', 'input_cat_verifyII.dat', 'input_cat_verifyIII.dat', 'input_cat_verifyIV.dat', 'input_cat_verifyII.fits', 'input_cat_verifyIV.fits']), \
                   ('AXE_CONFIG_PATH', 'CONF', ['verificationConfI.conf', 'constSensI.fits', 'mef_c4.00000_x-0.38167_y1.08146.fits', 'mef_c4.00000_x0.28625_y1.17167.fits']), \
                   ('AXE_OUTPUT_PATH', 'OUTPUT'), ('AXE_OUTSIM_PATH', 'OUTSIM'), \
                   #('AXE_SIMDATA_PATH', 'SIMDATA', ['wfc3_ir_f125w_tpass_m01.dat']), \
                   ('AXE_DRIZZLE_PATH', 'DRIZZLE')]

        # define the directory with the input data and make sure it exists
        self.dataDir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'verifyData'))
        if not os.path.isdir(self.dataDir):
            errMsg = 'File does not exist: %s!' % self.dataDir
            raise Exception(errMsg)
        
        # define a name for the run directory;
        # destroy any old version;
        # create a new one
        #self.runDir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'verifyTests'))
        # run test in source directory may cause trouble depending where the code is integrated (not necessery writable)
        # new path is defined relative, assuming the test would be ran in a appropiate directory
        self.runDir = os.path.abspath('./verifyTests')
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
                        errMsg = 'File does not exist: %s!' % inFile
                        raise Exception(errMsg)

                    # copy the file
                    shutil.copy(inFile, outFile)
        # create a subdir for tips tests
        if not os.path.isdir(os.path.join(self.runDir,'tips')):
            os.mkdir(os.path.join(self.runDir,'tips'))
        # create a subdir for tips tests
        if not os.path.isdir(os.path.join(self.runDir,'tips','wave')):
            os.mkdir(os.path.join(self.runDir,'tips','wave'))
        self.tipsDir = os.path.join(self.runDir,'tips','wave')

    def tearDown(self):
        # check the mop up flag
        if self.doRemove:
            # tear down the run directory
            if os.path.isdir(self.runDir):
                shutil.rmtree(self.runDir, ignore_errors=True, onerror=None)

    def testGaussModSpec(self):
        """
        Gaussian objects with model spectra
        """
        import math
        import axesim
        import verify

        # make the simulation
        axesim.simdispim(incat='input_cat_verifyII.dat', config='verificationConfI.conf',
                         dispim_name='test_verify_Flux_GaussModspec.fits', model_spectra='input_line.spc.fits',
                         exptime=10., bck_flux=0.0, detector=self.detectorFlag, silent=self.silentFlag)

        # check that the output image exists
        resultFile = os.path.join(os.environ['AXE_OUTSIM_PATH'], 'test_verify_Flux_GaussModspec.fits')
        self.assertTrue(os.path.isfile(resultFile), 'Output file does not exist: %s!' % resultFile)

        # compute the simulated flux and extract the flux values from the simulated image
        simVals, fitVals, cogVals = verify.verifyII(os.path.join(os.environ['AXE_OUTSIM_PATH'],'test_verify_Flux_GaussModspec.fits'), 
                                           os.path.join(os.environ['AXE_IMAGE_PATH'],'input_cat_verifyII.dat'), 
                                           os.path.join(os.environ['AXE_CONFIG_PATH'],'verificationConfI.conf'),
                                           inSpec=os.path.join(os.environ['AXE_IMAGE_PATH'],'input_line.spc.fits'))
        
        # go over all objects
        for index in range(len(simVals)):

            # make sure the difference is small
            #self.assertLess(relDiff1, 1.0E-03)
            #print '%.3f <-> %.3f : %.3f %.2f <-> %.2f : %.2f' % (simVals[index]['center'], fitVals[index][1], fitVals[index][1]-simVals[index]['center'],simVals[index]['fwhm'], fitVals[index][2]*5.0/2.35482, fitVals[index][2]*5.0/2.35482-simVals[index]['fwhm']) 
            #print '%.3f <-> %.3f : %.3f %.2f <-> %.2f : %.2f' % (simVals[index]['center'], fitVals[index][1], fitVals[index][1]-simVals[index]['center'], simVals[index]['center'], cogVals[index], cogVals[index]-simVals[index]['center']) 
            self.assertLess(math.fabs(fitVals[index][1]-simVals[index]['center']), 0.5)
            self.assertLess(math.fabs(cogVals[index]-simVals[index]['center']), 0.5)

    def testGaussModSpec_tips(self):
        """
        Gaussian objects with model spectra at TIPS level
        """
        import math
        import tips
        import verify

        inCat = os.path.join(os.environ['AXE_IMAGE_PATH'],'input_cat_verifyII.fits')
        inSpc = os.path.join(os.environ['AXE_IMAGE_PATH'],'input_line.spc.fits')
        
        obs = tips.Observation(inCat, inSpc, inCatForm='TIPS', inSpcForm='aXeSIM', norm=True)
        obs.loadFromFile(os.path.join(os.environ['AXE_CONFIG_PATH'],'verificationConfI.fits'))
        obs.runSimulation(workDir=self.tipsDir)

        # check that the output image exists
        resultFile = os.path.join(self.tipsDir,'OUTSIM', 'input_cat_verifyII_WFC3_IR_00_v1_verify_d300914_IMG.fits')
        self.assertTrue(os.path.isfile(resultFile), 'Output file does not exist: %s!' % resultFile)

        axesimCat = os.path.join(self.tipsDir,'DATA','input_cat_verifyII_WFC3_IR_00.cat')
        verify.getInitialModIndex(inCat, axesimCat)
        
        # compute the simulated flux and extract the flux values from the simulated image
        simVals, fitVals, cogVals = verify.verifyII(os.path.join(self.tipsDir,'OUTSIM','input_cat_verifyII_WFC3_IR_00_v1_verify_d300914_IMG.fits'), 
                                                    axesimCat, os.path.join(self.tipsDir,'CONF','WFC3_IR_00_v1_verify_d300914.conf'), inSpec=inSpc)
        
        # go over all objects
        for index in range(len(simVals)):

            # make sure the difference is small
            #self.assertLess(relDiff1, 1.0E-03)
            #print '%.3f <-> %.3f : %.3f %.2f <-> %.2f : %.2f' % (simVals[index]['center'], fitVals[index][1], fitVals[index][1]-simVals[index]['center'],simVals[index]['fwhm'], fitVals[index][2]*5.0/2.35482, fitVals[index][2]*5.0/2.35482-simVals[index]['fwhm']) 
            #print '%.3f <-> %.3f : %.3f %.2f <-> %.2f : %.2f' % (simVals[index]['center'], fitVals[index][1], fitVals[index][1]-simVals[index]['center'], simVals[index]['center'], cogVals[index], cogVals[index]-simVals[index]['center']) 
            self.assertLess(math.fabs(fitVals[index][1]-simVals[index]['center']), 0.5)
            self.assertLess(math.fabs(cogVals[index]-simVals[index]['center']), 0.5)

    @unittest.skipIf(vtipslt2, "not supported in with tips < 2.0")
    def testStarsModSpec(self):
        """
        Stellar objects with model spectra
        """
        import math
        import axesim
        import verify

        # make the simulation
        axesim.simdispim(incat='input_cat_verifyIII.dat', config='verificationConfI.conf',
                         dispim_name='test_verify_Flux_starsModspec.fits', model_images='input_stars_imgs.fits', model_spectra='input_line.spc.fits',
                         psf_file='mef_c4.00000_x0.28625_y1.17167.fits', exptime=10., bck_flux=0.0, detector=self.detectorFlag, silent=self.silentFlag)

        # check that the output image exists
        resultFile = os.path.join(os.environ['AXE_OUTSIM_PATH'], 'test_verify_Flux_starsModspec.fits')
        self.assertTrue(os.path.isfile(resultFile), 'Output file does not exist: %s!' % resultFile)

        # compute the simulated flux and extract the flux values from the simulated image
        simVals, fitVals, cogVals = verify.verifyII(os.path.join(os.environ['AXE_OUTSIM_PATH'],'test_verify_Flux_starsModspec.fits'), 
                                           os.path.join(os.environ['AXE_IMAGE_PATH'],'input_cat_verifyIII.dat'), 
                                           os.path.join(os.environ['AXE_CONFIG_PATH'],'verificationConfI.conf'),
                                           inSpec=os.path.join(os.environ['AXE_IMAGE_PATH'],'input_line.spc.fits'),
                                           inModel=os.path.join(os.environ['AXE_IMAGE_PATH'],'input_stars_imgs.fits'),
                                           inPSF=os.path.join(os.environ['AXE_CONFIG_PATH'],'mef_c4.00000_x-0.38167_y1.08146.fits'))
        
        # go over all objects
        for index in range(len(simVals)):

            # make sure the difference is small
            #self.assertLess(relDiff1, 1.0E-03)
            #print simVals[index]['center'], ' <-> ', cogVals[index][1], ' : ', cogVals[index][1]-simVals[index]['center']
            #print simVals[index]['fwhm'], ' <-> ', cogVals[index][2]*5.0/2.35482, ' : ', cogVals[index][2]*5.0/2.35482-simVals[index]['fwhm']
            #print '%.3f <-> %.3f : %.3f %.2f <-> %.2f : %.2f' % (simVals[index]['center'], fitVals[index][1], fitVals[index][1]-simVals[index]['center'],simVals[index]['fwhm'], fitVals[index][2]*5.0/2.35482, fitVals[index][2]*5.0/2.35482-simVals[index]['fwhm']) 
            #print '%.3f <-> %.3f : %.3f %.2f <-> %.2f : %.2f' % (simVals[index]['center'], fitVals[index][1], fitVals[index][1]-simVals[index]['center'], simVals[index]['center'], cogVals[index], cogVals[index]-simVals[index]['center']) 
            self.assertLess(math.fabs(fitVals[index][1]-simVals[index]['center']), 0.5)
            self.assertLess(math.fabs(cogVals[index]-simVals[index]['center']), 0.7)
            

    def testModImgSpec(self):
        """
        Model images with input spectra
        """
        import math
        import axesim
        import verify
        
        # make the simulation
        axesim.simdispim(incat='input_cat_verifyIV.dat', config='verificationConfI.conf',
                         dispim_name='test_verify_Flux_ModimgSpec.fits', model_images='galaxyThumbs.fits', model_spectra='input_line.spc.fits',
                         exptime=10., bck_flux=0.0, detector=self.detectorFlag, silent=self.silentFlag)

        # check that the output image exists
        resultFile = os.path.join(os.environ['AXE_OUTSIM_PATH'], 'test_verify_Flux_ModimgSpec.fits')
        self.assertTrue(os.path.isfile(resultFile), 'Output file does not exist: %s!' % resultFile)

        # compute the simulated flux and extract the flux values from the simulated image
        simVals, fitVals, cogVals = verify.verifyII(os.path.join(os.environ['AXE_OUTSIM_PATH'],'test_verify_Flux_ModimgSpec.fits'), 
                                          os.path.join(os.environ['AXE_IMAGE_PATH'],'input_cat_verifyIV.dat'), 
                                          os.path.join(os.environ['AXE_CONFIG_PATH'],'verificationConfI.conf'),
                                          inSpec=os.path.join(os.environ['AXE_IMAGE_PATH'],'input_line.spc.fits'),
                                          inModel=os.path.join(os.environ['AXE_IMAGE_PATH'],'galaxyThumbs.fits'))
        
        # go over all objects
        for index in range(len(simVals)):

            # make sure the difference is small
            #self.assertLess(relDiff1, 1.0E-03)
            #print simVals[index]['center'], ' <-> ', cogVals[index][1], ' : ', cogVals[index][1]-simVals[index]['center']
            #print simVals[index]['fwhm'], ' <-> ', cogVals[index][2]*5.0/2.35482, ' : ', cogVals[index][2]*5.0/2.35482-simVals[index]['fwhm']
            #print '%.3f <-> %.3f : %.3f %.2f <-> %.2f : %.2f' % (simVals[index]['center'], fitVals[index][1], fitVals[index][1]-simVals[index]['center'],simVals[index]['fwhm'], fitVals[index][2]*5.0/2.35482, fitVals[index][2]*5.0/2.35482-simVals[index]['fwhm']) 
            #print '%.3f <-> %.3f : %.3f %.2f <-> %.2f : %.2f' % (simVals[index]['center'], fitVals[index][1], fitVals[index][1]-simVals[index]['center'], simVals[index]['center'], cogVals[index], cogVals[index]-simVals[index]['center']) 
            self.assertLess(math.fabs(fitVals[index][1]-simVals[index]['center']), 0.5)
            self.assertLess(math.fabs(cogVals[index]-simVals[index]['center']), 0.5)
            
    def testModImgSpec_tips(self):
        """
        Model images with input spectra at TIPS level
        """
        import math
        import axesim
        import verify
        
        inCat = os.path.join(os.environ['AXE_IMAGE_PATH'],'input_cat_verifyIV.fits')
        inSpc = os.path.join(os.environ['AXE_IMAGE_PATH'],'input_line.spc.fits')
        inThm = os.path.join(os.environ['AXE_IMAGE_PATH'],'galaxyThumbs.fits')
        
        obs = tips.Observation(inCat, inSpc, inCatForm='TIPS', inSpcForm='aXeSIM', norm=True, inThmDir=inThm)
        obs.loadFromFile(os.path.join(os.environ['AXE_CONFIG_PATH'],'verificationConfI.fits'))
        obs.runSimulation(workDir=self.tipsDir)

        # check that the output image exists
        resultFile = os.path.join(self.tipsDir,'OUTSIM', 'input_cat_verifyIV_WFC3_IR_00_v1_verify_d300914_IMG.fits')
        self.assertTrue(os.path.isfile(resultFile), 'Output file does not exist: %s!' % resultFile)
        
        axesimCat = os.path.join(self.tipsDir,'DATA','input_cat_verifyIV_WFC3_IR_00.cat')
        verify.getInitialModIndex(inCat, axesimCat)

        # compute the simulated flux and extract the flux values from the simulated image
        simVals, fitVals, cogVals = verify.verifyII(os.path.join(self.tipsDir,'OUTSIM','input_cat_verifyIV_WFC3_IR_00_v1_verify_d300914_IMG.fits'), 
                                                    axesimCat, os.path.join(self.tipsDir,'CONF','WFC3_IR_00_v1_verify_d300914.conf'),
                                                    inSpec=inSpc, inModel=inThm)
        
        # go over all objects
        for index in range(len(simVals)):

            # make sure the difference is small
            #self.assertLess(relDiff1, 1.0E-03)
            #print '%.3f <-> %.3f : %.3f %.2f <-> %.2f : %.2f' % (simVals[index]['center'], fitVals[index][1], fitVals[index][1]-simVals[index]['center'],simVals[index]['fwhm'], fitVals[index][2]*5.0/2.35482, fitVals[index][2]*5.0/2.35482-simVals[index]['fwhm']) 
            #print '%.3f <-> %.3f : %.3f %.2f <-> %.2f : %.2f' % (simVals[index]['center'], fitVals[index][1], fitVals[index][1]-simVals[index]['center'], simVals[index]['center'], cogVals[index], cogVals[index]-simVals[index]['center']) 
            self.assertLess(math.fabs(fitVals[index][1]-simVals[index]['center']), 0.5)
            self.assertLess(math.fabs(cogVals[index]-simVals[index]['center']), 0.5)
    
    @unittest.skipIf(vtipslt2, "not supported in with tips < 2.0")
    def testModImgSpecPSF(self):
        """
        Model images with input spectra
        """
        import math
        import axesim
        import verify
        
        # make the simulation
        axesim.simdispim(incat='input_cat_verifyIV.dat', config='verificationConfI.conf',
                         dispim_name='test_verify_Flux_ModimgSpecPSF.fits', model_images='galaxyThumbs.fits', model_spectra='input_line.spc.fits',
                         psf_file='mef_c4.00000_x-0.38167_y1.08146.fits', exptime=10., bck_flux=0.0, detector=self.detectorFlag, silent=self.silentFlag)

        # check that the output image exists
        resultFile = os.path.join(os.environ['AXE_OUTSIM_PATH'], 'test_verify_Flux_ModimgSpecPSF.fits')
        self.assertTrue(os.path.isfile(resultFile), 'Output file does not exist: %s!' % resultFile)

        # compute the simulated flux and extract the flux values from the simulated image
        simVals, fitVals, cogVals = verify.verifyII(os.path.join(os.environ['AXE_OUTSIM_PATH'],'test_verify_Flux_ModimgSpecPSF.fits'), 
                                                    os.path.join(os.environ['AXE_IMAGE_PATH'],'input_cat_verifyIV.dat'), 
                                                    os.path.join(os.environ['AXE_CONFIG_PATH'],'verificationConfI.conf'),
                                                    inSpec=os.path.join(os.environ['AXE_IMAGE_PATH'],'input_line.spc.fits'),
                                                    inModel=os.path.join(os.environ['AXE_IMAGE_PATH'],'galaxyThumbs.fits'),
                                                    inPSF=os.path.join(os.environ['AXE_CONFIG_PATH'],'mef_c4.00000_x-0.38167_y1.08146.fits'))
        
        # go over all objects
        for index in range(len(simVals)):

            # make sure the difference is small
            #self.assertLess(relDiff1, 1.0E-03)
            #print simVals[index]['center'], ' <-> ', cogVals[index][1], ' : ', cogVals[index][1]-simVals[index]['center']
            #print simVals[index]['fwhm'], ' <-> ', cogVals[index][2]*5.0/2.35482, ' : ', cogVals[index][2]*5.0/2.35482-simVals[index]['fwhm']
            #print '%.3f <-> %.3f : %.3f %.2f <-> %.2f : %.2f' % (simVals[index]['center'], fitVals[index][1], fitVals[index][1]-simVals[index]['center'],simVals[index]['fwhm'], fitVals[index][2]*5.0/2.35482, fitVals[index][2]*5.0/2.35482-simVals[index]['fwhm']) 
            #print '%.3f <-> %.3f : %.3f %.2f <-> %.2f : %.2f' % (simVals[index]['center'], fitVals[index][1], fitVals[index][1]-simVals[index]['center'], simVals[index]['center'], cogVals[index], cogVals[index]-simVals[index]['center']) 
            self.assertLess(math.fabs(fitVals[index][1]-simVals[index]['center']), 0.5)
            self.assertLess(math.fabs(cogVals[index]-simVals[index]['center']), 0.5)
