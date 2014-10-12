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
import unittest

def tips_atest():
    from testverify.testVerifyFlux  import Test_VerifyFluxBasic
    from testverify.testVerifyWave  import Test_VerifyWaveBasic
    #from testverify.testVerifyDispFF import Test_VerifyDispFFBasic

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test_VerifyFluxBasic))
    suite.addTest(unittest.makeSuite(Test_VerifyWaveBasic))
    #suite.addTest(unittest.makeSuite(Test_VerifyDispFFBasic))

    return suite
    
if __name__ == '__main__':
        unittest.TextTestRunner(verbosity=2).run(tips_atest())
