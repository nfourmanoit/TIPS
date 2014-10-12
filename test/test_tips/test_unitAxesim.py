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
    from testaxesim.testaxesimDisp     import Test_AxesimDispBasic
    from testaxesim.testaxesimDir      import Test_AxesimDirBasic
    #from testaxesim.testaxesimDirDisp  import Test_AxesimDirDispBasic

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test_AxesimDispBasic))
    suite.addTest(unittest.makeSuite(Test_AxesimDirBasic))
    #suite.addTest(unittest.makeSuite(Test_AxesimDirDispBasic))

    return suite
    
if __name__ == '__main__':
        unittest.TextTestRunner(verbosity=2).run(tips_atest())
