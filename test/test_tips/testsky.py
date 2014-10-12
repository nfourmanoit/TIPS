"""
@author: Julien Zoubian
@organization: CPPM / LAM
@license: Gnu Public Licence
@contact: zoubian@cppm.in2p3.fr
"""

import asciidata
import pyfits
import numpy
import os
import shutil
import tips

import unittest

class Test_TipsSource(unittest.TestCase):
        def setUp(self):
                self.dataDir = os.path.abspath(os.path.dirname(__file__)+'/../data/')+'/'

        def test01_getCatCol(self):
                ssky = tips.SkySources(inCatDir=self.dataDir+"CMC_test.fits", inSpcDir=self.dataDir+"CMC_test.spc.fits")
                # test to load and read fits catalog (TIPS format)
                cat = pyfits.open(self.dataDir+"CMC_test.fits")
                test = ssky.getCatCol("RA")
                check = numpy.asarray(cat[1].data.field("RA"))
                diff = numpy.sum((test-check)**2)
                error_message = 'Error in SkySources Class, with fits catalog, method getCatCol, RA column'
                self.assertAlmostEqual(diff, 0.0, places=30, msg=error_message)
                test = ssky.getCatCol("A_SKY")
                check = numpy.asarray(cat[1].data.field("A_SKY"))
                diff = numpy.sum((test-check)**2)
                error_message = 'Error in SkySources Class, with fits catalog, method getCatCol, A_SKY column'
                self.assertAlmostEqual(diff, 0.0, places=30, msg=error_message)
                cat.close()
                ssky.close()

        def test02_getCatCol(self):
                ssky = tips.SkySources(inCatDir=self.dataDir+"CMC_test.out", inSpcDir=self.dataDir+"CMC_test.spc.fits", inCatForm='CMC')
                # test to load and read fits catalog (TIPS format)
                cat = asciidata.open(self.dataDir+"CMC_test.out")
                test = ssky.getCatCol("RA")
                check = numpy.asarray(cat["RA"].tonumpy())
                diff = numpy.sum((test-check)**2)
                error_message = 'Error in SkySources Class, with ascii catalog, method getCatCol, RA column'
                self.assertAlmostEqual(diff, 0.0, places=30, msg=error_message)
                test = ssky.getCatCol("A_SKY")
                check = numpy.asarray(cat["A_IMAGE"].tonumpy())*0.03
                diff = numpy.sum((test-check)**2)
                error_message = 'Error in SkySources Class, with ascii catalog, method getCatCol, A_SKY column'
                self.assertAlmostEqual(diff, 0.0, places=30, msg=error_message)
                ssky.close()

        def test03_getSpc(self):
                ssky = tips.SkySources(inCatDir=self.dataDir+"CMC_test.fits", inSpcDir=self.dataDir+"CMC_test.spc.fits")
                hdus = ssky.getCatCol("MODSPEC")
                ids = ssky.getCatCol("NUMBER")
                tspc = numpy.random.randint(low=0, high=ssky.nSources, size=10)
                spcs = pyfits.open(self.dataDir+"CMC_test.spc.fits")
                for i in tspc:
                        (w, f) = ssky.getSpcIdent(ids[i])
                        wCheck = numpy.asarray(spcs[hdus[i]].data.field("lambda"))
                        fCheck = numpy.asarray(spcs[hdus[i]].data.field("flux"))
                        wDiff = numpy.sum((w-wCheck)**2)
                        fDiff = numpy.sum((f-fCheck)**2)
                        error_message = 'Error in SkySources Class, with CMC spectra, method getSpc, lambda column'
                        self.assertAlmostEqual(wDiff, 0.0, places=30, msg=error_message)
                        error_message = 'Error in SkySources Class, with CMC spectra, method getSpc, flux column'
                        self.assertAlmostEqual(fDiff, 0.0, places=30, msg=error_message)
                spcs.close()
                ssky.close()

        def test04_getSpc(self):
                ssky = tips.SkySources(inCatDir=self.dataDir+"CMC_test.fits", inSpcDir=self.dataDir+"CMC_test.axespc.fits", inSpcForm='aXeSIM')
                hdus = ssky.getCatCol("MODSPEC")
                tspc = numpy.random.randint(low=0, high=ssky.nSources, size=10)
                spcs = pyfits.open(self.dataDir+"CMC_test.axespc.fits")
                for i in tspc:
                        (w, f) = ssky.getSpcIndex(i)
                        wCheck = numpy.asarray(spcs[hdus[i]].data.field("WAV_NM"))*10.0
                        fCheck = numpy.asarray(spcs[hdus[i]].data.field("FLUX"))
                        wDiff = numpy.sum((w-wCheck)**2)
                        fDiff = numpy.sum((f-fCheck)**2)
                        error_message = 'Error in SkySources Class, with CMC spectra, method getSpc, lambda column'
                        self.assertAlmostEqual(wDiff, 0.0, places=30, msg=error_message)
                        error_message = 'Error in SkySources Class, with CMC spectra, method getSpc, flux column'
                        self.assertAlmostEqual(fDiff, 0.0, places=30, msg=error_message)
                spcs.close()
                ssky.close()

        def test05_reset(self):
                ssky = tips.SkySources(inCatDir=self.dataDir+"CMC_test.fits", inSpcDir=self.dataDir+"CMC_test.spc.fits")
                # test to load and read fits catalog (TIPS format)
                test11 = ssky.getCatCol("RA")
                test21 = ssky.getCatCol("A_SKY")
                hdus = ssky.getCatCol("MODSPEC")
                ids = ssky.getCatCol("NUMBER")
                test31w = []
                test31f = []
                tspc = numpy.random.randint(low=0, high=ssky.nSources, size=10)
                for i in tspc:
                        (w, f) = ssky.getSpcIdent(ids[i])
                        test31w.append(w)
                        test31f.append(f)
                # reset with ascii cat and axesim spectra
                ssky.reset(newCatDir=self.dataDir+"CMC_test.out", newCatForm='CMC', newSpcDir=self.dataDir+"CMC_test.axespc.fits", newSpcForm='aXeSIM')
                test12 = ssky.getCatCol("RA")
                diff1 = numpy.sum((test11-test12)**2)
                error_message = 'Error in SkySources Class, with reset, method getCatCol, RA column'
                self.assertAlmostEqual(diff1, 0.0, places=30, msg=error_message)
                ssky.close()

#       def test06_getSpc(self):
#               ssky = tips.SkySources(inCatDir=self.dataDir+"CMC_SplitFits_test.fits", inSpcForm='SplitFits')
#               rsky = tips.SkySources(inCatDir=self.dataDir+"CMC_test.fits", inSpcDir=self.dataDir+"CMC_test.spc.fits")
#               rids = rsky.getCatCol("NUMBER")
#               tspc = numpy.random.randint(low=0, high=ssky.nSources, size=10)
#               for i in tspc:
#                       (w, f) = ssky.getSpcIndex(i)
#                       (wCheck, fCheck) = rsky.getSpcIdent(rids[i])
#                       wDiff = numpy.sum((w-wCheck)**2)
#                       fDiff = numpy.sum((f-fCheck)**2)
#                       error_message = 'Error in SkySources Class, with CMC spectra, method getSpc, lambda column'
#                       self.assertAlmostEqual(wDiff, 0.0, places=30, msg=error_message)
#                       error_message = 'Error in SkySources Class, with CMC spectra, method getSpc, flux column'
#                       self.assertAlmostEqual(fDiff, 0.0, places=30, msg=error_message)
#               rsky.close()
#               ssky.close()
#
#       def test07_getSpc(self):
#               ssky = tips.SkySources(inCatDir=self.dataDir+"CMC_SplitAscii_test.fits", inSpcForm='SplitAscii')
#               rsky = tips.SkySources(inCatDir=self.dataDir+"CMC_test.fits", inSpcDir=self.dataDir+"CMC_test.spc.fits")
#               ids = ssky.getCatCol("NUMBER")
#               tspc = numpy.random.randint(low=0, high=ssky.nSources, size=10)
#               for i in tspc:
#                       (w, f) = ssky.getSpcIdent(ids[i])
#                       (wCheck, fCheck) = rsky.getSpcIndex(i)
#                       wDiff = numpy.sum((w-wCheck)**2)
#                       fDiff = numpy.sum((f-fCheck)**2)
#                       error_message = 'Error in SkySources Class, with CMC spectra, method getSpc, lambda column'
#                       self.assertAlmostEqual(wDiff, 0.0, places=30, msg=error_message)
#                       error_message = 'Error in SkySources Class, with CMC spectra, method getSpc, flux column'
#                       self.assertAlmostEqual(fDiff, 0.0, places=30, msg=error_message)
#               rsky.close()
#               ssky.close()

class Test_TipsNoise(unittest.TestCase):
        def setUp(self):
                self.dataDir = os.path.abspath(os.path.dirname(__file__)+'/../data/')+'/'

        def test01_cst(self):
                nsky = tips.SkyNoise()
                nsky.addContanteNoise(noiseValue=1e-17, lambda_min=1000.0, lambda_max=25000.0, lambda_step=100.0)
                fDiff = numpy.sum((nsky.flux-1e-17)**2)
                error_message = 'Error in SkyNoise Class, method addContanteNoise'
                self.assertAlmostEqual(fDiff, 0.0, places=30, msg=error_message)
                nsky.close()

        def test02_ald(self):
                nsky = tips.SkyNoise()
                nsky.addAldering02Noise(scale=1.0, lambda_min=1000.0, lambda_max=25000.0, lambda_step=1000.0)
                wCheck = [1000., 2000., 3000., 4000., 5000., 6000., 7000., 8000., 9000.,
                          10000., 11000., 12000., 13000., 14000., 15000., 16000., 17000.,
                          18000., 19000., 20000., 21000., 22000., 23000., 24000.]
                fCheck = [0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                          1.75792361e-18, 1.75792361e-18, 4.14285754e-18, 3.50186984e-18,
                          2.96005650e-18, 2.50207314e-18, 2.11494949e-18, 1.78772206e-18,
                          1.51112364e-18, 1.27732085e-18, 1.07969229e-18, 9.12641052e-19,
                          7.71436174e-19, 6.52078679e-19, 5.51188312e-19, 4.65907820e-19,
                          3.93822024e-19, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00]
                wDiff = numpy.sum((nsky.wave-wCheck)**2)
                fDiff = numpy.sum((nsky.flux-fCheck)**2)
                error_message = 'Error in SkyNoise Class, method addAldering02Noise'
                self.assertAlmostEqual(wDiff, 0.0, places=30, msg=error_message)
                self.assertAlmostEqual(fDiff, 0.0, places=30, msg=error_message)
                nsky.close()
        
        def test03_spc(self):
                nsky = tips.SkyNoise()
                nsky.addAldering02Noise(scale=1.0, lambda_min=1000.0, lambda_max=25000.0, lambda_step=100.0)
                wCheck = nsky.wave
                fCheck = nsky.flux
                nsky = tips.SkyNoise()
                nsky.addSpcNoise(self.dataDir+"noise_spc.dat")
                wDiff = numpy.sum((nsky.wave-wCheck)**2)
                fDiff = numpy.sum((nsky.flux-fCheck)**2)
                error_message = 'Error in SkyNoise Class, method addSpcNoise'
                self.assertAlmostEqual(wDiff, 0.0, places=30, msg=error_message)
                self.assertAlmostEqual(fDiff, 0.0, places=30, msg=error_message)
                nsky.close()

        def test04_add(self):
                nsky = tips.SkyNoise()
                nsky.addSpcNoise(self.dataDir+"noise_spc.fits")
                wCheck = nsky.wave
                fCheck = nsky.flux
                nsky = tips.SkyNoise(lambda_min=1000.0, lambda_max=25000.0, lambda_step=1000.0)
                nsky.addContanteNoise(noiseValue=1e-17)
                nsky.addAldering02Noise(scale=2.0)
                wDiff = numpy.sum((nsky.wave-wCheck)**2)
                fDiff = numpy.sum((nsky.flux-fCheck)**2)
                error_message = 'Error in SkyNoise Class with combined noise'
                self.assertAlmostEqual(wDiff, 0.0, places=30, msg=error_message)
                self.assertAlmostEqual(fDiff, 0.0, places=30, msg=error_message)
                nsky.close()

        def test05_add2(self):
                nsky = tips.SkyNoise()
                nsky.addSpcNoise(self.dataDir+"noise_spc.fits")
                wCheck = nsky.wave
                fCheck = nsky.flux
                nsky = tips.SkyNoise(lambda_min=1000.0, lambda_max=25000.0, lambda_step=1000.0)
                nsky.addContanteNoise(noiseValue=1e-17)
                nsky.addAldering02Noise()
                nsky.addSpcNoise(self.dataDir+"noise_spc.dat",interp_warn=False)
                wDiff = numpy.sum((nsky.wave-wCheck)**2)
                fDiff = numpy.sum((nsky.flux-fCheck)**2)
                error_message = 'Error in SkyNoise Class with combined noise'
                self.assertAlmostEqual(wDiff, 0.0, places=30, msg=error_message)
                self.assertAlmostEqual(fDiff, 0.0, places=30, msg=error_message)
                nsky.close()

class Test_TipsAbs(unittest.TestCase):
        def setUp(self):
                self.dataDir = os.path.abspath(os.path.dirname(__file__)+'/../data/')+'/'
                self.wCheck = [1590., 2590., 3590., 4590., 5590., 6590., 7590., 8590., 9590.,
                        10590., 11590., 12590., 13590., 14590., 15590., 16590., 17590., 18590.,
                        19590., 20590., 21590., 22590., 23590., 24590., 25590., 26590., 27590.,
                        28590., 29590., 30590., 31590., 32590., 33590., 34590., 35590., 36590.,
                        37590., 38590., 39590., 40590.]
                self.eCheck = [7.80435, 6.65068, 4.94566, 3.90548, 3.05867, 2.36978, 1.95812, 1.58073,
                        1.27968, 1.12862, 1.04492, 0.96122, 0.87752, 0.79382, 0.71012, 0.62642,
                        0.54272, 0.45902, 0.37532, 0.33849, 0.33422, 0.32996, 0.3257, 0.32144,
                        0.31717, 0.31291, 0.30865, 0.30439, 0.30012, 0.29586, 0.2916, 0.28734,
                        0.28307, 0.27881, 0.27455, 0.27029, 0.26602, 0.26176, 0.2575, 0.25324]
                self.tCheck = [0.4873332, 0.54196695, 0.63412314, 0.69788008, 0.7544895, 0.80391253,
                        0.83497832, 0.86451155, 0.88881792, 0.90127059, 0.90824539, 0.91527416,
                        0.92235732, 0.9294953, 0.93668853, 0.94393741, 0.9512424, 0.95860392,
                        0.96602241, 0.96930488, 0.96968617, 0.97006671, 0.9704474, 0.97082824,
                        0.97121012, 0.97159126, 0.97197255, 0.97235399, 0.97273647, 0.97311821,
                        0.9735001, 0.97388214, 0.97426522, 0.97464756, 0.97503005, 0.97541269,
                        0.97579637, 0.97617931, 0.9765624, 0.97694564]

        def test01_ext(self):
                asky = tips.SkyAbs()
                asky.setFromExt(self.dataDir+"ext_seaton.fits", ebv=0.1)
                wDiff = numpy.sum((asky.wave-self.wCheck)**2)
                eDiff = numpy.sum((asky.ext-self.eCheck)**2)
                tDiff = numpy.sum((asky.trans-self.tCheck)**2)
                ebvDiff = (asky.ebv-0.1)**2
                error_message = 'Error in SkyAbs Class, method setFromExt'
                self.assertAlmostEqual(wDiff, 0.0, places=30, msg=error_message)
                self.assertAlmostEqual(eDiff, 0.0, places=30, msg=error_message)
                self.assertAlmostEqual(tDiff, 0.0, places=15, msg=error_message)
                self.assertAlmostEqual(ebvDiff, 0.0, places=30, msg=error_message)
                asky.close()

        def test02_trans(self):
                asky = tips.SkyAbs()
                asky.setFromTrans(self.dataDir+"ext_seaton.fits")
                wDiff = numpy.sum((asky.wave-self.wCheck)**2)
                tDiff = numpy.sum((asky.trans-self.tCheck)**2)
                error_message = 'Error in SkyAbs Class, method setFromTrans'
                self.assertAlmostEqual(wDiff, 0.0, places=30, msg=error_message)
                self.assertAlmostEqual(tDiff, 0.0, places=15, msg=error_message)
                asky.close()

        def test03_interp(self):
                asky = tips.SkyAbs()
                asky.setFromExt(self.dataDir+"ext_seaton.fits", ebv=0.1)
                asky.setFromExt(self.dataDir+"ext_seaton.dat", ebv=0.1, interp_warn=False)
                wDiff = numpy.sum((asky.wave-self.wCheck)**2)
                eDiff = numpy.sum((asky.ext-self.eCheck)**2)
                tDiff = numpy.sum((asky.trans-self.tCheck)**2)
                ebvDiff = (asky.ebv-0.1)**2
                error_message = 'Error in SkyAbs Class, method setFromExt with interpolation'
                self.assertAlmostEqual(wDiff, 0.0, places=30, msg=error_message)
                self.assertAlmostEqual(eDiff, 0.0, places=30, msg=error_message)
                self.assertAlmostEqual(tDiff, 0.0, places=15, msg=error_message)
                self.assertAlmostEqual(ebvDiff, 0.0, places=30, msg=error_message)
                asky.close()

        def test04_reset(self):
                asky = tips.SkyAbs()
                asky.setFromExt(self.dataDir+"ext_seaton.fits", ebv=0.1)
                asky.resetEBV(0.5)
                wCheck = [1590., 2590., 3590., 4590., 5590., 6590., 7590., 8590., 9590.,
                        10590., 11590., 12590., 13590., 14590., 15590., 16590., 17590., 18590.,
                        19590., 20590., 21590., 22590., 23590., 24590., 25590., 26590., 27590.,
                        28590., 29590., 30590., 31590., 32590., 33590., 34590., 35590., 36590.,
                        37590., 38590., 39590., 40590.]
                eCheck = [7.80435, 6.65068, 4.94566, 3.90548, 3.05867, 2.36978, 1.95812, 1.58073,
                        1.27968, 1.12862, 1.04492, 0.96122, 0.87752, 0.79382, 0.71012, 0.62642,
                        0.54272, 0.45902, 0.37532, 0.33849, 0.33422, 0.32996, 0.3257, 0.32144,
                        0.31717, 0.31291, 0.30865, 0.30439, 0.30012, 0.29586, 0.2916, 0.28734,
                        0.28307, 0.27881, 0.27455, 0.27029, 0.26602, 0.26176, 0.2575, 0.25324]
                tCheck = [0.02748717, 0.04675887, 0.10253402, 0.1655404, 0.24449276, 0.33577163,
                        0.40585977, 0.48289644, 0.55470745, 0.59466996, 0.61803917, 0.64232674,
                        0.66756875, 0.69380272, 0.72106763, 0.74940399, 0.7788539, 0.80946113,
                        0.84127116, 0.85566152, 0.85734575, 0.85902935, 0.86071625, 0.86240646,
                        0.86410397, 0.86580083, 0.86750103, 0.86920457, 0.87091546, 0.8726257,
                        0.8743393, 0.87605627, 0.87778064, 0.87950437, 0.88123147, 0.88296197,
                        0.88469994, 0.88643725, 0.88817798, 0.88992212]
                wDiff = numpy.sum((asky.wave-wCheck)**2)
                eDiff = numpy.sum((asky.ext-eCheck)**2)
                tDiff = numpy.sum((asky.trans-tCheck)**2)
                ebvDiff = (asky.ebv-0.5)**2
                error_message = 'Error in SkyAbs Class, method resetEBV'
                self.assertAlmostEqual(wDiff, 0.0, places=30, msg=error_message)
                self.assertAlmostEqual(eDiff, 0.0, places=30, msg=error_message)
                self.assertAlmostEqual(tDiff, 0.0, places=15, msg=error_message)
                self.assertAlmostEqual(ebvDiff, 0.0, places=30, msg=error_message)
                asky.close()

if __name__ == '__main__':
        unittest.main()

