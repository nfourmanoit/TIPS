"""
@author: Julien Zoubian
@organization: CPPM / LAM
@license: Gnu Public Licence
@contact: zoubian@cppm.in2p3.fr
"""

import os
import sys
import tips

def mkdir(dir):
  # function to make directory
  if os.path.exists(dir):
    if not os.path.isdir(dir):
      print """
Error: %s alredy exist and is not a directory!
      """
      sys.exit()
  else:
      os.mkdir(dir)

import unittest

class Test_TipsDetector(unittest.TestCase):
        def setUp(self):
                self.rn   = 6.0
                self.qe   = 0.75
                self.dc   = 0.1
                self.nx   = 2040
                self.ny   = 2040
                self.scale = 0.3
                self.size = 18.0

        def test01_load(self):
                det = tips.Detector()
                det.loadEUCLIDdefault(1)
                error_message='Error in Detector class, loadEUCLIDdefault'
                self.assertAlmostEqual(det.rn   , self.rn   , places=30, msg=error_message)
                self.assertAlmostEqual(det.qe   , self.qe   , places=30, msg=error_message)
                self.assertAlmostEqual(det.dc   , self.dc   , places=30, msg=error_message)
                self.assertAlmostEqual(det.nx   , self.nx   , places=30, msg=error_message)
                self.assertAlmostEqual(det.ny   , self.ny   , places=30, msg=error_message)
                self.assertAlmostEqual(det.scale, self.scale, places=30, msg=error_message)
                self.assertAlmostEqual(det.size , self.size , places=30, msg=error_message)
                det.close()
                
class Test_TipsBeam(unittest.TestCase):
        def test01_loadGblueA(self):
                beam = tips.Beam()
                beam.loadEUCLIDGblueA()
                self.assertEqual(beam.idientier, 'A')
                self.assertAlmostEqual(beam.xstart, 0)
                self.assertAlmostEqual(beam.xend, 392)
                self.assertEqual(len(beam.dydx), 2)
                self.assertAlmostEqual(beam.dydx[0], 0.0)
                self.assertAlmostEqual(beam.dydx[1], 0.0)
                self.assertAlmostEqual(beam.xoff, -195.0)
                self.assertAlmostEqual(beam.yoff, 0.0)
                self.assertEqual(len(beam.dldp), 2)
                self.assertAlmostEqual(beam.dldp[0], 10870.0)
                self.assertAlmostEqual(beam.dldp[1], 9.8)
                self.assertEqual(beam.sensitivity, 'Gblue_noDET.sens.fits')
                beam.close()

        def test02_loadGredA(self):
                beam = tips.Beam()
                beam.loadEUCLIDGredA()
                self.assertEqual(beam.idientier, 'A')
                self.assertAlmostEqual(beam.xstart, 0)
                self.assertAlmostEqual(beam.xend, 584)
                self.assertEqual(len(beam.dydx), 2)
                self.assertAlmostEqual(beam.dydx[0], 0.0)
                self.assertAlmostEqual(beam.dydx[1], 0.0)
                self.assertAlmostEqual(beam.xoff, -291.0)
                self.assertAlmostEqual(beam.yoff, 0.0)
                self.assertEqual(len(beam.dldp), 2)
                self.assertAlmostEqual(beam.dldp[0], 14420.0)
                self.assertAlmostEqual(beam.dldp[1], 9.8)
                self.assertEqual(beam.sensitivity, 'Gred_noDET.sens.fits')
                beam.close()

class Test_TipsGrism(unittest.TestCase):
        def test01_loadGblue(self):
                grism = tips.Grism()
                grism.loadEUCLIDGblue()
                self.assertEqual(grism.idientier, 'GBLUE0')
                self.assertAlmostEqual(grism.lambdaRef, 1250.0)
                self.assertAlmostEqual(grism.sig1, 0.12)
                self.assertAlmostEqual(grism.sig2, 0.66)
                self.assertAlmostEqual(grism.c, 0.75)
                self.assertEqual(len(grism.beams), 1)
                self.assertEqual(grism.beams[0].idientier, 'A')
                grism.close()

        def test02_loadGred(self):
                grism = tips.Grism()
                grism.loadEUCLIDGred()
                self.assertEqual(grism.idientier, 'GRED0')
                self.assertAlmostEqual(grism.lambdaRef, 1750.0)
                self.assertAlmostEqual(grism.sig1, 0.15)
                self.assertAlmostEqual(grism.sig2, 0.84)
                self.assertAlmostEqual(grism.c, 0.75)
                self.assertEqual(len(grism.beams), 1)
                self.assertEqual(grism.beams[0].idientier, 'A')
                grism.close()

class Test_TipsSpectro(unittest.TestCase):
        def test01_loadGblue0(self):
                spectro = tips.Spectrometer()
                spectro.loadEUCLIDGblue0()
                self.assertAlmostEqual(spectro.idientier , 'NISP')
                self.assertEqual(spectro.grism.idientier, 'GBLUE0')
                self.assertAlmostEqual(spectro.telarea , 10066.0)
                self.assertAlmostEqual(spectro.wcs.crpix1 , 0.0)
                self.assertAlmostEqual(spectro.wcs.crpix2 , 0.0)
                self.assertAlmostEqual(spectro.wcs.crval1 , 0.0)
                self.assertAlmostEqual(spectro.wcs.crval2 , 0.0)
                self.assertAlmostEqual(spectro.wcs.cd11 , spectro.detector.scale/3600.0)
                self.assertAlmostEqual(spectro.wcs.cd12 , 0.0)
                self.assertAlmostEqual(spectro.wcs.cd21 , 0.0)
                self.assertAlmostEqual(spectro.wcs.cd22 , spectro.detector.scale/3600.0)
                self.assertAlmostEqual(spectro.wcs.orient , 0.0)
                self.assertFalse(spectro.rot90)
                spectro.close()

        def test02_loadGred0(self):
                spectro = tips.Spectrometer()
                spectro.loadEUCLIDGred0()
                self.assertAlmostEqual(spectro.idientier , 'NISP')
                self.assertEqual(spectro.grism.idientier, 'GRED0')
                self.assertAlmostEqual(spectro.telarea , 10066.0)
                self.assertAlmostEqual(spectro.wcs.crpix1 , 0.0)
                self.assertAlmostEqual(spectro.wcs.crpix2 , 0.0)
                self.assertAlmostEqual(spectro.wcs.crval1 , 0.0)
                self.assertAlmostEqual(spectro.wcs.crval2 , 0.0)
                self.assertAlmostEqual(spectro.wcs.cd11 , spectro.detector.scale/3600.0)
                self.assertAlmostEqual(spectro.wcs.cd12 , 0.0)
                self.assertAlmostEqual(spectro.wcs.cd21 , 0.0)
                self.assertAlmostEqual(spectro.wcs.cd22 , spectro.detector.scale/3600.0)
                self.assertAlmostEqual(spectro.wcs.orient , 0.0)
                self.assertFalse(spectro.rot90)
                spectro.close()

        def test03_loadGblue90(self):
                spectro = tips.Spectrometer()
                spectro.loadEUCLIDGblue90()
                self.assertAlmostEqual(spectro.idientier , 'NISP')
                self.assertEqual(spectro.grism.idientier, 'GBLUE90')
                self.assertAlmostEqual(spectro.telarea , 10066.0)
                self.assertAlmostEqual(spectro.wcs.crpix1 , 0.0)
                self.assertAlmostEqual(spectro.wcs.crpix2 , 0.0)
                self.assertAlmostEqual(spectro.wcs.crval1 , 0.0)
                self.assertAlmostEqual(spectro.wcs.crval2 , 0.0)
                self.assertAlmostEqual(spectro.wcs.cd11 , spectro.detector.scale/3600.0)
                self.assertAlmostEqual(spectro.wcs.cd12 , 0.0)
                self.assertAlmostEqual(spectro.wcs.cd21 , 0.0)
                self.assertAlmostEqual(spectro.wcs.cd22 , spectro.detector.scale/3600.0)
                self.assertAlmostEqual(spectro.wcs.orient , 0.0)
                self.assertTrue(spectro.rot90)
                spectro.close()

        def test04_loadGred90(self):
                spectro = tips.Spectrometer()
                spectro.loadEUCLIDGred90()
                self.assertAlmostEqual(spectro.idientier , 'NISP')
                self.assertEqual(spectro.grism.idientier, 'GRED90')
                self.assertAlmostEqual(spectro.telarea , 10066.0)
                self.assertAlmostEqual(spectro.wcs.crpix1 , 0.0)
                self.assertAlmostEqual(spectro.wcs.crpix2 , 0.0)
                self.assertAlmostEqual(spectro.wcs.crval1 , 0.0)
                self.assertAlmostEqual(spectro.wcs.crval2 , 0.0)
                self.assertAlmostEqual(spectro.wcs.cd11 , spectro.detector.scale/3600.0)
                self.assertAlmostEqual(spectro.wcs.cd12 , 0.0)
                self.assertAlmostEqual(spectro.wcs.cd21 , 0.0)
                self.assertAlmostEqual(spectro.wcs.cd22 , spectro.detector.scale/3600.0)
                self.assertAlmostEqual(spectro.wcs.orient , 0.0)
                self.assertTrue(spectro.rot90)
                spectro.close()

        def test05_writeaXeConf(self):
                spectro = tips.Spectrometer()
                mkdir('./testtips')
                mkdir('./testtips/CONF')
                spectro.loadEUCLIDGblue0()
                spectro.writeaXeConf('./testtips/CONF/Gblue0.conf')
                self.assertTrue(os.path.isfile('./testtips/CONF/Gblue0.conf'))
                spectro.loadEUCLIDGred0()
                spectro.writeaXeConf('./testtips/CONF/Gred0.conf')
                self.assertTrue(os.path.isfile('./testtips/CONF/Gred0.conf'))
                spectro.loadEUCLIDGblue90()
                spectro.writeaXeConf('./testtips/CONF/Gblue90.conf')
                self.assertTrue(os.path.isfile('./testtips/CONF/Gblue90.conf'))
                spectro.loadEUCLIDGred90()
                spectro.writeaXeConf('./testtips/CONF/Gred90.conf')
                self.assertTrue(os.path.isfile('./testtips/CONF/Gred90.conf'))
                spectro.close()
                self.doCleanups()

class Test_TipsFocalPlan(unittest.TestCase):
        def test01_load(self):
                spectro = tips.FocalPlan()
                spectro.loadEUCLIDDefault()
                #self.assertAlmostEqual(spectro.ra0 , 0)
                #self.assertAlmostEqual(spectro.dec0 , 0)
                self.assertAlmostEqual(spectro.xstep , 3000.0/18.0)
                self.assertAlmostEqual(spectro.ystep , 6000.0/18.0)
                self.assertEqual(len(spectro.spectros) , 16)
                spectro.close()

if __name__ == '__main__':
        unittest.main()
