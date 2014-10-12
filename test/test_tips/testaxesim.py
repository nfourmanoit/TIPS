"""
@author: Julien Zoubian
@organization: CPPM / LAM
@license: Gnu Public Licence
@contact: zoubian@cppm.in2p3.fr
"""

import os
import shutil
import tips
import axesim
from axesim import axesimerror

import unittest

# check scipy version and print warning is < 0.12
import scipy
scipy_version = (scipy.__version__).split('.')
if int(scipy_version[0])<1 and int(scipy_version[1])<12:
    vscipylt12 = True
else:
    vscipylt12 = False

class Test_Simdispim(unittest.TestCase):
        def _mkdir(self, dir):
            # function to make directory
            if os.path.exists(dir):
                if not os.path.isdir(dir):
                    print """
Error: %s alredy exist and is not a directory!
                    """
                    sys.exit()
            else:
                    os.mkdir(dir)
 
        def setUp(self):
                # set data path
                self.dataDir = os.path.abspath(os.path.dirname(__file__)+'/../data/')+'/'
  
                self._mkdir('./testaxesim')
                os.environ['AXE_IMAGE_PATH'] = './testaxesim/DATA/'
                os.environ['AXE_CONFIG_PATH']  = './testaxesim/CONF/'
                os.environ['AXE_OUTPUT_PATH']  = './testaxesim/OUTPUT/'
                os.environ['AXE_OUTSIM_PATH']  = './testaxesim/OUTSIM/'
                os.environ['AXE_SIMDATA_PATH'] = './testaxesim/SIMDATA/'
                os.environ['AXE_DRIZZLE_PATH'] = './testaxesim/DRIZZLE/'
                self._mkdir('./testaxesim/DATA')
                shutil.copy(self.dataDir+'input_cat_test.dat',os.environ['AXE_IMAGE_PATH'])

        def test00_init(self):
                # prepare path
                self.assertTrue(os.path.isdir('./testaxesim'))

                self._mkdir('./testaxesim/CONF')
                self._mkdir('./testaxesim/OUTPUT')
                self._mkdir('./testaxesim/OUTSIM')
                self._mkdir('./testaxesim/SIMDATA')
                self._mkdir('./testaxesim/DRIZZLE')

                shutil.copy(self.dataDir+'input_cat_test.spc.fits',os.environ['AXE_IMAGE_PATH'])
                self.assertTrue(os.path.isfile(os.environ['AXE_IMAGE_PATH']+'input_cat_test.spc.fits'))

        def test01_img1(self):
                shutil.copy(self.dataDir+'axesim_d1.conf',os.environ['AXE_CONFIG_PATH'])
                shutil.copy(self.dataDir+'sensfunc_d1.fits',os.environ['AXE_CONFIG_PATH'])
                axesim.simdispim(incat='input_cat_test.dat', config='axesim_d1.conf', dispim_name='output_test_img1.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux=0.5, detector=False)
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img1.fits'))

        def test02_img2(self):
                shutil.copy(self.dataDir+'axesim_d2.conf',os.environ['AXE_CONFIG_PATH'])
                shutil.copy(self.dataDir+'sensfunc_d2.fits',os.environ['AXE_CONFIG_PATH'])
                axesim.simdispim(incat='input_cat_test.dat', config='axesim_d2.conf', dispim_name='output_test_img2.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux=0.5, detector=False)
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img2.fits'))

        def test03_img3(self):
                shutil.copy(self.dataDir+'axesim_d3.conf',os.environ['AXE_CONFIG_PATH'])
                axesim.simdispim(incat='input_cat_test.dat', config='axesim_d3.conf', dispim_name='output_test_img3.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux=0.5, detector=False)
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img3.fits'))

        def test04_img4(self):
                shutil.copy(self.dataDir+'axesim_d4.conf',os.environ['AXE_CONFIG_PATH'])
                axesim.simdispim(incat='input_cat_test.dat', config='axesim_d4.conf', dispim_name='output_test_img4.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux=0.5, detector=False)
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img4.fits'))

        def test05_img1_PSF(self):
                shutil.copy(self.dataDir+'axesim_d1_PSF.conf',os.environ['AXE_CONFIG_PATH'])
                axesim.simdispim(incat='input_cat_test.dat', config='axesim_d1_PSF.conf', dispim_name='output_test_img1_PSF.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux=0.5, detector=False)
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img1_PSF.fits'))

        def test06_img2_PSF(self):
                shutil.copy(self.dataDir+'axesim_d2_PSF.conf',os.environ['AXE_CONFIG_PATH'])
                axesim.simdispim(incat='input_cat_test.dat', config='axesim_d2_PSF.conf', dispim_name='output_test_img2_PSF.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux=0.5, detector=False)
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img2_PSF.fits'))

        def test07_img3_PSF(self):
                shutil.copy(self.dataDir+'axesim_d3_PSF.conf',os.environ['AXE_CONFIG_PATH'])
                axesim.simdispim(incat='input_cat_test.dat', config='axesim_d3_PSF.conf', dispim_name='output_test_img3_PSF.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux=0.5, detector=False)
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img3_PSF.fits'))

        def test08_img4_PSF(self):
                shutil.copy(self.dataDir+'axesim_d4_PSF.conf',os.environ['AXE_CONFIG_PATH'])
                axesim.simdispim(incat='input_cat_test.dat', config='axesim_d4_PSF.conf', dispim_name='output_test_img4_PSF.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux=0.5, detector=False)
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img4_PSF.fits'))

        def test09_img1_2PSF(self):
                shutil.copy(self.dataDir+'axesim_d1_2PSF.conf',os.environ['AXE_CONFIG_PATH'])
                axesim.simdispim(incat='input_cat_test.dat', config='axesim_d1_2PSF.conf', dispim_name='output_test_img1_2PSF.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux=0.5, detector=False)
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img1_2PSF.fits'))

        def test10_img2_2PSF(self):
                shutil.copy(self.dataDir+'axesim_d2_2PSF.conf',os.environ['AXE_CONFIG_PATH'])
                axesim.simdispim(incat='input_cat_test.dat', config='axesim_d2_2PSF.conf', dispim_name='output_test_img2_2PSF.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux=0.5, detector=False)
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img2_2PSF.fits'))

        def test11_img3_2PSF(self):
                shutil.copy(self.dataDir+'axesim_d3_2PSF.conf',os.environ['AXE_CONFIG_PATH'])
                axesim.simdispim(incat='input_cat_test.dat', config='axesim_d3_2PSF.conf', dispim_name='output_test_img3_2PSF.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux=0.5, detector=False)
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img3_2PSF.fits'))

        def test12_img4_2PSF(self):
                shutil.copy(self.dataDir+'axesim_d4_2PSF.conf',os.environ['AXE_CONFIG_PATH'])
                axesim.simdispim(incat='input_cat_test.dat', config='axesim_d4_2PSF.conf', dispim_name='output_test_img4_2PSF.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux=0.5, detector=False)
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img4_2PSF.fits'))

        def test13_img1_det(self):
                shutil.copy(self.dataDir+'RN_map.fits',os.environ['AXE_CONFIG_PATH'])
                shutil.copy(self.dataDir+'DC_map.fits',os.environ['AXE_CONFIG_PATH'])
                shutil.copy(self.dataDir+'QE_map.fits',os.environ['AXE_CONFIG_PATH'])
                shutil.copy(self.dataDir+'axesim_d1_det.conf',os.environ['AXE_CONFIG_PATH'])
                axesim.simdispim(incat='input_cat_test.dat', config='axesim_d1_2PSF.conf', dispim_name='output_test_img1_det.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux=0.5)
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img1_det.fits'))

        def test14_img2_det(self):
                shutil.copy(self.dataDir+'axesim_d2_det.conf',os.environ['AXE_CONFIG_PATH'])
                axesim.simdispim(incat='input_cat_test.dat', config='axesim_d2_2PSF.conf', dispim_name='output_test_img2_det.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux=0.5)
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img2_det.fits'))

        def test15_img3_det(self):
                shutil.copy(self.dataDir+'axesim_d3_det.conf',os.environ['AXE_CONFIG_PATH'])
                axesim.simdispim(incat='input_cat_test.dat', config='axesim_d3_2PSF.conf', dispim_name='output_test_img3_det.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux=0.5)
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img3_det.fits'))

        def test16_img4_det(self):
                shutil.copy(self.dataDir+'axesim_d4_det.conf',os.environ['AXE_CONFIG_PATH'])
                axesim.simdispim(incat='input_cat_test.dat', config='axesim_d4_2PSF.conf', dispim_name='output_test_img4_det.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux=0.5)
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img4_det.fits'))

        def test17_img1_det2(self):
                shutil.copy(self.dataDir+'SB_map.fits',os.environ['AXE_CONFIG_PATH'])
                axesim.simdispim(incat='input_cat_test.dat', config='axesim_d1_det.conf', dispim_name='output_test_img1_det2.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux='SB_map.fits')
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img1_det2.fits'))

        def test18_img2_det2(self):
                axesim.simdispim(incat='input_cat_test.dat', config='axesim_d2_det.conf', dispim_name='output_test_img2_det2.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux='SB_map.fits')
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img2_det2.fits'))

        def test19_img3_det2(self):
                axesim.simdispim(incat='input_cat_test.dat', config='axesim_d3_det.conf', dispim_name='output_test_img3_det2.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux='SB_map.fits')
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img3_det2.fits'))

        def test20_img4_det2(self):
                axesim.simdispim(incat='input_cat_test.dat', config='axesim_d4_det.conf', dispim_name='output_test_img4_det2.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux='SB_map.fits')
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img4_det2.fits'))

        def test21_img1_det3(self):
                shutil.copy(self.dataDir+'axesim_d1_cos.conf',os.environ['AXE_CONFIG_PATH'])
                axesim.simdispim(incat='input_cat_test.dat', config='axesim_d1_cos.conf', dispim_name='output_test_img1_det3.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux=1.0, norm=False)
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img1_det3.fits'))

        def test22_img2_det3(self):
                shutil.copy(self.dataDir+'axesim_d2_cos.conf',os.environ['AXE_CONFIG_PATH'])
                shutil.copy(self.dataDir+'cosmics_0.fits',os.environ['AXE_CONFIG_PATH'])
                axesim.simdispim(incat='input_cat_test.dat', config='axesim_d2_cos.conf', dispim_name='output_test_img2_det3.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux='SB_map.fits')
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img2_det3.fits'))

        def test23_img3_det3(self):
                shutil.copy(self.dataDir+'axesim_d3_cos.conf',os.environ['AXE_CONFIG_PATH'])
                axesim.simdispim(incat='input_cat_test.dat', config='axesim_d3_cos.conf', dispim_name='output_test_img3_det3.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux='SB_map.fits')
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img3_det3.fits'))

        def test24_img4_det3(self):
                shutil.copy(self.dataDir+'axesim_d4_cos.conf',os.environ['AXE_CONFIG_PATH'])
                axesim.simdispim(incat='input_cat_test.dat', config='axesim_d4_cos.conf', dispim_name='output_test_img4_det3.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux='SB_map.fits', norm=False)
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img4_det3.fits'))
                
        def test25_img1_zero(self):
                shutil.copy(self.dataDir+'axesim_d1_zero.conf',os.environ['AXE_CONFIG_PATH'])
                shutil.copy(self.dataDir+'sensfunc_d11.fits',os.environ['AXE_CONFIG_PATH'])
                axesim.simdispim(incat='input_cat_test.dat', config='axesim_d1_zero.conf', dispim_name='output_test_img1_zero.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux=1.0, norm=False)
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img1_zero.fits'))

        def test26_img2_zero(self):
                shutil.copy(self.dataDir+'axesim_d2_zero.conf',os.environ['AXE_CONFIG_PATH'])
                shutil.copy(self.dataDir+'sensfunc_d21.fits',os.environ['AXE_CONFIG_PATH'])
                axesim.simdispim(incat='input_cat_test.dat', config='axesim_d2_zero.conf', dispim_name='output_test_img2_zero.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux='SB_map.fits')
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img2_zero.fits'))

        def test27_img3_zero(self):
                shutil.copy(self.dataDir+'axesim_d3_zero.conf',os.environ['AXE_CONFIG_PATH'])
                axesim.simdispim(incat='input_cat_test.dat', config='axesim_d3_zero.conf', dispim_name='output_test_img3_zero.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux='SB_map.fits')
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img3_zero.fits'))

        def test28_img4_zero(self):
                shutil.copy(self.dataDir+'axesim_d4_zero.conf',os.environ['AXE_CONFIG_PATH'])
                axesim.simdispim(incat='input_cat_test.dat', config='axesim_d4_zero.conf', dispim_name='output_test_img4_zero.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux='SB_map.fits', norm=False)
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img4_zero.fits'))

        @unittest.skipIf(vscipylt12, "not supported in with scipy < 0.12.0")
        def test29_img1(self):
                shutil.copy(self.dataDir+'thumbnails.fits',os.environ['AXE_IMAGE_PATH'])
                shutil.copy(self.dataDir+'input_cat_thumbs.dat',os.environ['AXE_IMAGE_PATH'])
                axesim.simdispim(incat='input_cat_thumbs.dat', config='axesim_d1.conf', dispim_name='output_test_img1_thumbs.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux=0.5, detector=False, model_images='thumbnails.fits')
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img1_thumbs.fits'))

        @unittest.skipIf(vscipylt12, "not supported in with scipy < 0.12.0")
        def test30_img2(self):
                axesim.simdispim(incat='input_cat_thumbs.dat', config='axesim_d2.conf', dispim_name='output_test_img2_thumbs.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux=0.5, detector=False, model_images='thumbnails.fits')
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img2_thumbs.fits'))

        @unittest.skipIf(vscipylt12, "not supported in with scipy < 0.12.0")
        def test31_img3(self):
                axesim.simdispim(incat='input_cat_thumbs.dat', config='axesim_d3.conf', dispim_name='output_test_img3_thumbs.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux=0.5, model_images='thumbnails.fits')
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img3_thumbs.fits'))

        @unittest.skipIf(vscipylt12, "not supported in with scipy < 0.12.0")
        def test32_img4(self):
                axesim.simdispim(incat='input_cat_thumbs.dat', config='axesim_d4.conf', dispim_name='output_test_img4_thumbs.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux=0.5, model_images='thumbnails.fits')
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img4_thumbs.fits'))

        @unittest.skipIf(vscipylt12, "not supported in with scipy < 0.12.0")
        def test33_img1(self):
                axesim.simdispim(incat='input_cat_thumbs.dat', config='axesim_d1_PSF.conf', dispim_name='output_test_img1_thumbs_PSF.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux=0.5, detector=False, model_images='thumbnails.fits')
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img1_thumbs_PSF.fits'))

        @unittest.skipIf(vscipylt12, "not supported in with scipy < 0.12.0")
        def test34_img2(self):
                axesim.simdispim(incat='input_cat_thumbs.dat', config='axesim_d2_PSF.conf', dispim_name='output_test_img2_thumbs_PSF.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux='SB_map.fits', model_images='thumbnails.fits')
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img2_thumbs_PSF.fits'))

        @unittest.skipIf(vscipylt12, "not supported in with scipy < 0.12.0")
        def test35_img3(self):
                axesim.simdispim(incat='input_cat_thumbs.dat', config='axesim_d3_PSF.conf', dispim_name='output_test_img3_thumbs_PSF.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux=0.5, model_images='thumbnails.fits')
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img3_thumbs_PSF.fits'))

        @unittest.skipIf(vscipylt12, "not supported in with scipy < 0.12.0")
        def test36_img4(self):
                axesim.simdispim(incat='input_cat_thumbs.dat', config='axesim_d4_PSF.conf', dispim_name='output_test_img4_thumbs_PSF.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux=0.5, model_images='thumbnails.fits')
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img4_thumbs_PSF.fits'))

        @unittest.skipIf(vscipylt12, "not supported in with scipy < 0.12.0")
        def test37_img1(self):
                axesim.simdispim(incat='input_cat_thumbs.dat', config='axesim_d1_2PSF.conf', dispim_name='output_test_img1_thumbs_2PSF.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux=0.5, model_images='thumbnails.fits')
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img1_thumbs_2PSF.fits'))

        @unittest.skipIf(vscipylt12, "not supported in with scipy < 0.12.0")
        def test38_img2(self):
                axesim.simdispim(incat='input_cat_thumbs.dat', config='axesim_d2_2PSF.conf', dispim_name='output_test_img2_thumbs_2PSF.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux=0.5, detector=False, model_images='thumbnails.fits')
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img2_thumbs_2PSF.fits'))

        @unittest.skipIf(vscipylt12, "not supported in with scipy < 0.12.0")
        def test39_img3(self):
                axesim.simdispim(incat='input_cat_thumbs.dat', config='axesim_d3_2PSF.conf', dispim_name='output_test_img3_thumbs_2PSF.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux='SB_map.fits', model_images='thumbnails.fits')
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img3_thumbs_2PSF.fits'))

        @unittest.skipIf(vscipylt12, "not supported in with scipy < 0.12.0")
        def test40_img4(self):
                axesim.simdispim(incat='input_cat_thumbs.dat', config='axesim_d4_2PSF.conf', dispim_name='output_test_img4_thumbs_2PSF.fits',
                                model_spectra='input_cat_test.spc.fits', bck_flux=0.5, model_images='thumbnails.fits')
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img4_thumbs_2PSF.fits'))

        def test41_img1(self):
                axesim.simdispim(incat=None, config='axesim_d1.conf', dispim_name='output_test_img1_dark.fits',
                                model_spectra=None, bck_flux=0.5, detector=True, model_images=None)
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img1_dark.fits'))               

        def test42_img2_dark(self):
                axesim.simdispim(incat=None, config='axesim_d2_PSF.conf', dispim_name='output_test_img2_PSF_dark.fits',
                                model_spectra=None, bck_flux=0.5, detector=True, model_images=None)
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img2_PSF_dark.fits'))

        def test43_img3_PSF_dark(self):
                axesim.simdispim(incat=None, config='axesim_d3_PSF.conf', dispim_name='output_test_img3_PSF_dark.fits',
                                model_spectra=None, bck_flux=0.5, detector=False, model_images=None)
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img3_PSF_dark.fits'))               

        def test44_img4_2PSF_dark(self):
                axesim.simdispim(incat=None, config='axesim_d4_2PSF.conf', dispim_name='output_test_img4_2PSF_dark.fits',
                                model_spectra=None, bck_flux=0.5, detector=True, model_images=None)
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img4_2PSF_dark.fits'))               

        def test45_img1_det_dark(self):
                axesim.simdispim(incat=None, config='axesim_d1_det.conf', dispim_name='output_test_img1_det_dark.fits',
                                model_spectra=None, bck_flux=0.5, detector=True, model_images=None)
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img1_det_dark.fits'))               

        def test46_img2_det_dark(self):
                axesim.simdispim(incat=None, config='axesim_d2_det.conf', dispim_name='output_test_img2_det_dark.fits',
                                model_spectra=None, bck_flux='SB_map.fits', detector=True, model_images=None)
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img2_det_dark.fits'))               

        def test47_img3_cos_dark(self):
                axesim.simdispim(incat=None, config='axesim_d3_cos.conf', dispim_name='output_test_img3_cos_dark.fits',
                                model_spectra=None, bck_flux=0.5, detector=True, model_images=None)
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img3_cos_dark.fits'))
 
        def test48_img4_zero_dark(self):
                axesim.simdispim(incat=None, config='axesim_d4_zero.conf', dispim_name='output_test_img4_zero_dark.fits',
                                model_spectra=None, bck_flux='SB_map.fits', detector=True, model_images=None)
                self.assertTrue(os.path.isfile(os.environ['AXE_OUTSIM_PATH']+'output_test_img4_zero_dark.fits'))               
 
if __name__ == '__main__':
        unittest.main()

