"""
@author: Julien Zoubian
@organization: CPPM
@copyright: Gnu Public Licence
@contact: zoubian@cppm.in2p3.fr

Function to run the TIPS unit test.
"""

import unittest

def tips_utest():
        from test.testsky import Test_TipsSource
        from test.testsky import Test_TipsNoise
        from test.testsky import Test_TipsAbs
        from test.testinstrument import Test_TipsDetector
        from test.testinstrument import Test_TipsBeam
        from test.testinstrument import Test_TipsGrism
        from test.testinstrument import Test_TipsSpectro
        from test.testinstrument import Test_TipsFocalPlan

        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(Test_TipsSource))
        suite.addTest(unittest.makeSuite(Test_TipsNoise))
        suite.addTest(unittest.makeSuite(Test_TipsAbs))
        suite.addTest(unittest.makeSuite(Test_TipsDetector))
        suite.addTest(unittest.makeSuite(Test_TipsBeam))
        suite.addTest(unittest.makeSuite(Test_TipsGrism))
        suite.addTest(unittest.makeSuite(Test_TipsSpectro))
        suite.addTest(unittest.makeSuite(Test_TipsFocalPlan))

        return suite

if __name__ == '__main__':
        unittest.TextTestRunner(verbosity=2).run(tips_utest())
