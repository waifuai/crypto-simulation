import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'affiliate/src')))
from simulation import token_simulation_step, affiliate_simulation_step, run_simulation

class TestSimulation(unittest.TestCase):

    def test_simulation_functions_exist(self):
        self.assertTrue(callable(token_simulation_step))
        self.assertTrue(callable(affiliate_simulation_step))
        self.assertTrue(callable(run_simulation))

if __name__ == '__main__':
    unittest.main()