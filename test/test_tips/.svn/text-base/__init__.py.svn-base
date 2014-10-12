"""
@author: Julien Zoubian
@organization: CPPM / LAM
@license: Gnu Public Licence
@contact: zoubian@cppm.in2p3.fr

Initialize the TIPS test.
"""

import test_unit
import test_preintegration 
import test_integration
import test_integration_pp 
import test_fullsystem
import test_unitAxesim
import test_Verify

def run():
        test_unit.unittest.TextTestRunner(verbosity=2).run(test_unit.tips_utest())                            # runs OK
        test_preintegration.unittest.TextTestRunner(verbosity=2).run(test_preintegration.tips_pretest())      # runs OK
        test_integration.unittest.TextTestRunner(verbosity=2).run(test_integration.tips_inttest())            # runs OK
        #test_integration_pp.unittest.TextTestRunner(verbosity=2).run(test_integration.tips_inttest_pp())
        #test_fullsystem.unittest.TextTestRunner(verbosity=2).run(test_integration.tips_fulltest())
        test_unitAxesim.unittest.TextTestRunner(verbosity=2).run(test_unitAxesim.tips_atest())                # runs OK
        test_Verify.unittest.TextTestRunner(verbosity=2).run(test_Verify.tips_atest())                        # runs OK
