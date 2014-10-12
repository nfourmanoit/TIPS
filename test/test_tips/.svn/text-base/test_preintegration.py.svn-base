"""
@author: Julien Zoubian
@organization: CPPM
@copyright: Gnu Public Licence
@contact: zoubian@cppm.in2p3.fr

Function to run the TIPS pre-integration test.
"""

import unittest

def tips_pretest():
        from test.testaxesim import Test_Simdispim

        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(Test_Simdispim))

        return suite

if __name__ == '__main__':
        unittest.TextTestRunner(verbosity=2).run(tips_pretest())
