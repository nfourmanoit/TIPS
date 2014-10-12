"""
@author: Julien Zoubian
@organization: CPPM
@copyright: Gnu Public Licence
@contact: zoubian@cppm.in2p3.fr

Function to run the TIPS integration test.
"""

import unittest

def tips_inttest():
        from test.testobservation import Test_TipsObservation

        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(Test_TipsObservation))

        return suite

if __name__ == '__main__':
        unittest.TextTestRunner(verbosity=2).run(tips_inttest())
