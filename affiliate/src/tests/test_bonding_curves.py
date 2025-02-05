import unittest
import sys
import os
from bonding_curves import linear_bonding_curve, exponential_bonding_curve, sigmoid_bonding_curve, root_bonding_curve, inverse_bonding_curve

class TestBondingCurves(unittest.TestCase):

    def test_bonding_curve_functions_exist(self):
        self.assertTrue(callable(linear_bonding_curve))
        self.assertTrue(callable(exponential_bonding_curve))
        self.assertTrue(callable(sigmoid_bonding_curve))
        self.assertTrue(callable(root_bonding_curve))
        self.assertTrue(callable(inverse_bonding_curve))

if __name__ == '__main__':
    unittest.main()