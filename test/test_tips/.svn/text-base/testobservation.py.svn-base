"""
@author: Julien Zoubian
@organization: CPPM / LAM
@license: Gnu Public Licence
@contact: zoubian@cppm.in2p3.fr
"""

import os
import shutil
import sys
import tips
import unittest
import pyfits

# check scipy version and print warning is < 0.12
import scipy
scipy_version = (scipy.__version__).split('.')
if int(scipy_version[0])<1 and int(scipy_version[1])<12:
    vscipylt12 = True
else:
    vscipylt12 = False

class Test_TipsObservation(unittest.TestCase):
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
               self._mkdir('./testtips')
               self.inCat = self.dataDir + 'CMC_test.fits'
               self.inSpc = self.dataDir + 'CMC_test.spc.fits'
               self.ra0 = 150.0
               self.dec0 = 2.6

       def test01_Gblue0(self):
               obs = tips.Observation(self.inCat, self.inSpc)
               obs.loadEUCLIDDefault(grismName='Gblue0', exptime=560.0, ra0=self.ra0, dec0=self.dec0)
               obs.runSimulation(workDir='./testtips')
               for i in range(4):
                       for j in range(4):
                            imgname = 'testtips/OUTSIM/CMC_test_NISP_GBLUE0_'+str(i)+str(j)+'_IMG.fits'
                            self.assertTrue(os.path.isfile(imgname), msg=imgname+' does not exist.')
                            img = pyfits.open(imgname)
                            self.assertEqual(len(img), 4, msg=imgname+' contains %d hdu, 4 was expected' % len(img))
               obs.close()
               
       def test02_Gblue90(self):
               self.ra0 += (100.0/3600.0)
               self.dec0 += (50.0/3600.0)
               obs = tips.Observation(self.inCat, self.inSpc)
               obs.loadEUCLIDDefault(grismName='Gblue90', exptime=560.0, ra0=self.ra0, dec0=self.dec0)
               spectroList = obs.getSpectros()
               for one in spectroList:
                       obs.runOneSim(one, workDir='./testtips')
               for i in range(4):
                       for j in range(4):
                            imgname = 'testtips/OUTSIM/CMC_test_NISP_GBLUE90_'+str(i)+str(j)+'_IMG.fits'
                            self.assertTrue(os.path.isfile(imgname), msg=imgname+' does not exist.')
                            img = pyfits.open(imgname)
                            self.assertEqual(len(img), 4, msg=imgname+' contains %d hdu, 4 was expected' % len(img))
               obs.close()
       
       def test03_Gred0(self):
               self.ra0 += (100.0/3600.0)
               obs = tips.Observation(self.inCat, self.inSpc)
               obs.loadEUCLIDDefault(grismName='Gred0', exptime=560.0, ra0=self.ra0, dec0=self.dec0)
               spectroList = obs.getSpectros()
               for one in spectroList:
                       obs.runOneSim(one, workDir='./testtips')        
               for i in range(4):
                       for j in range(4):
                            imgname = 'testtips/OUTSIM/CMC_test_NISP_GRED0_'+str(i)+str(j)+'_IMG.fits'
                            self.assertTrue(os.path.isfile(imgname), msg=imgname+' does not exist.')
                            img = pyfits.open(imgname)
                            self.assertEqual(len(img), 4, msg=imgname+' contains %d hdu, 4 was expected' % len(img))
               obs.close()
       
       def test04_Gred90(self):
               self.ra0 += (100.0/3600.0)
               obs = tips.Observation(self.inCat, self.inSpc)
               obs.loadEUCLIDDefault(grismName='Gred90', exptime=560.0, ra0=self.ra0, dec0=self.dec0)
               obs.runSimulation(workDir='./testtips')
               for i in range(4):
                       for j in range(4):
                            imgname = 'testtips/OUTSIM/CMC_test_NISP_GRED90_'+str(i)+str(j)+'_IMG.fits'
                            self.assertTrue(os.path.isfile(imgname), msg=imgname+' does not exist.')
                            img = pyfits.open(imgname)
                            self.assertEqual(len(img), 4, msg=imgname+' contains %d hdu, 4 was expected' % len(img))
               obs.close()
       
       def test05_Gblue0(self):
               self.ra0 = 150.0
               self.dec0 = 2.6
               shutil.copy(self.inCat, './testtips/CMC_test2.fits')
               inCat = './testtips/CMC_test2.fits'
               obs = tips.Observation(inCat, self.inSpc)
               obs.loadFromFile(self.dataDir + 'GBLUE_0.0_conf_v0.fits')
               obs.runSimulation(workDir='./testtips')
               for i in range(4):
                       for j in range(4):
                            imgname = 'testtips/OUTSIM/CMC_test2_NISP_GBLUE0_'+str(i)+str(j)+'_v0_IMG.fits'
                            self.assertTrue(os.path.isfile(imgname), msg=imgname+' does not exist.')
                            img = pyfits.open(imgname)
                            self.assertEqual(len(img), 4, msg=imgname+' contains %d hdu, 4 was expected' % len(img))
               obs.close()
               
       def test06_Gblue90(self):
               self.ra0 += (100.0/3600.0)
               self.dec0 += (50.0/3600.0)
               inCat = './testtips/CMC_test2.fits'
               obs = tips.Observation(inCat, self.inSpc)
               obs.loadFromFile(self.dataDir + 'GBLUE_90.0_conf_v0.fits', ra0=self.ra0, dec0=self.dec0, exptime=540.0)
               spectroList = obs.getSpectros()
               for one in spectroList:
                       obs.runOneSim(one, workDir='./testtips')
               for i in range(4):
                       for j in range(4):
                            imgname = 'testtips/OUTSIM/CMC_test2_NISP_GBLUE90_'+str(i)+str(j)+'_v0_IMG.fits'
                            self.assertTrue(os.path.isfile(imgname), msg=imgname+' does not exist.')
                            img = pyfits.open(imgname)
                            self.assertEqual(len(img), 4, msg=imgname+' contains %d hdu, 4 was expected' % len(img))
               obs.close()
       
       def test07_Gred0(self):
               self.ra0 += (100.0/3600.0)
               inCat = './testtips/CMC_test2.fits'
               obs = tips.Observation(inCat, self.inSpc)
               obs.loadFromFile(self.dataDir + 'GRED_0.0_conf_v0.fits', exptime=540.0)
               spectroList = obs.getSpectros()
               for one in spectroList:
                       obs.runOneSim(one, workDir='./testtips')        
               for i in range(4):
                       for j in range(4):
                            imgname = 'testtips/OUTSIM/CMC_test2_NISP_GRED0_'+str(i)+str(j)+'_v0_IMG.fits'
                            self.assertTrue(os.path.isfile(imgname), msg=imgname+' does not exist.')
                            img = pyfits.open(imgname)
                            self.assertEqual(len(img), 4, msg=imgname+' contains %d hdu, 4 was expected' % len(img))
               obs.close()
       
       def test08_Gred90(self):
               self.ra0 += (100.0/3600.0)
               inCat = './testtips/CMC_test2.fits'
               obs = tips.Observation(inCat, self.inSpc)
               obs.loadFromFile(self.dataDir + 'GRED_90.0_conf_v0.fits', ra0=self.ra0, exptime=540.0)
               obs.runSimulation(workDir='./testtips')
               for i in range(4):
                       for j in range(4):
                            imgname = 'testtips/OUTSIM/CMC_test2_NISP_GRED90_'+str(i)+str(j)+'_v0_IMG.fits'
                            self.assertTrue(os.path.isfile(imgname), msg=imgname+' does not exist.')
                            img = pyfits.open(imgname)
                            self.assertEqual(len(img), 4, msg=imgname+' contains %d hdu, 4 was expected' % len(img))
               obs.close()
               
       def test09_all(self):
               self.ra0 = 150.0
               self.dec0 = 2.6             
               shutil.copy(self.inCat, './testtips/CMC_test3.fits')
               inCat = './testtips/CMC_test3.fits'
               obs = tips.Observation(inCat, self.inSpc)
               obs.loadFromFile(self.dataDir + 'baseline_180713_conf_v1.fits', ra0=self.ra0, dec0=self.dec0)
               obs.runSimulation(workDir='./testtips')
               for gname in ['GBLUE0', 'GRED0', 'GBLUE90', 'GRED90']:
                    for i in range(4):
                        for j in range(4):
                            imgname = 'testtips/OUTSIM/CMC_test3_NISP_'+gname+'_'+str(i)+str(j)+'_v1_baseline_d180713_IMG.fits'
                            self.assertTrue(os.path.isfile(imgname), msg=imgname+' does not exist.')
                            img = pyfits.open(imgname)
                            self.assertEqual(len(img), 4, msg=imgname+' contains %d hdu, 4 was expected' % len(img))
               obs.close()
               
       @unittest.skipIf(vscipylt12, "not supported in with scipy < 0.12.0")
       def test10_all_thm(self):
               self.ra0 = 150.0
               self.dec0 = 2.6             
               shutil.copy(self.inCat, './testtips/CMC_test4.fits')
               inCat = './testtips/CMC_test4.fits'
               obs = tips.Observation(inCat, self.inSpc, inThmDir=self.dataDir + 'CMC_test.thm.fits')
               obs.loadFromFile(self.dataDir + 'baseline_180713_conf_v1.fits', ra0=self.ra0, dec0=self.dec0)
               obs.runSimulation(workDir='./testtips')
               for gname in ['GBLUE0', 'GRED0', 'GBLUE90', 'GRED90']:
                    for i in range(4):
                        for j in range(4):
                            imgname = 'testtips/OUTSIM/CMC_test4_NISP_'+gname+'_'+str(i)+str(j)+'_v1_baseline_d180713_IMG.fits'
                            self.assertTrue(os.path.isfile(imgname), msg=imgname+' does not exist.')
                            img = pyfits.open(imgname)
                            self.assertEqual(len(img), 4, msg=imgname+' contains %d hdu, 4 was expected' % len(img))
               obs.close()
               
       def test11_all_dark(self):
               self.ra0 = 150.0
               self.dec0 = 2.6             
               obs = tips.Observation()
               obs.loadFromFile(self.dataDir + 'baseline_180713_conf_v1.fits', ra0=self.ra0, dec0=self.dec0)
               obs.runSimulation(workDir='./testtips')
               for gname in ['GBLUE0', 'GRED0', 'GBLUE90', 'GRED90']:
                    for i in range(4):
                        for j in range(4):
                            imgname = 'testtips/OUTSIM/dark_NISP_'+gname+'_'+str(i)+str(j)+'_v1_baseline_d180713_IMG.fits'
                            self.assertTrue(os.path.isfile(imgname), msg=imgname+' does not exist.')
                            img = pyfits.open(imgname)
                            self.assertEqual(len(img), 4, msg=imgname+' contains %d hdu, 4 was expected' % len(img))
               obs.close()               
               
       def test12_all_nosrc(self):
               self.ra0 = 150.0
               self.dec0 = 2.6
               inCat = self.inCat.replace('.fits', '_half.fits')
               obs = tips.Observation(inCat, self.inSpc)
               obs.loadFromFile(self.dataDir + 'baseline_180713_conf_v1.fits', ra0=self.ra0, dec0=self.dec0)
               obs.runSimulation(workDir='./testtips')
               for gname in ['GBLUE0', 'GRED0', 'GBLUE90', 'GRED90']:
                    for i in range(4):
                        for j in range(4):
                            imgname = 'testtips/OUTSIM/CMC_test_half_NISP_'+gname+'_'+str(i)+str(j)+'_v1_baseline_d180713_IMG.fits'
                            self.assertTrue(os.path.isfile(imgname), msg=imgname+' does not exist.')
                            img = pyfits.open(imgname)
                            self.assertEqual(len(img), 4, msg=imgname+' contains %d hdu, 4 was expected' % len(img))
               obs.close()

if __name__ == '__main__':
       unittest.main()

