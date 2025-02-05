import unittest
import numpy as np
from bonding_curves import (
    linear_bonding_curve, 
    exponential_bonding_curve, 
    sigmoid_bonding_curve, 
    root_bonding_curve, 
    inverse_bonding_curve
)

class TestBondingCurves(unittest.TestCase):

    def test_bonding_curve_functions_exist(self):
        self.assertTrue(callable(linear_bonding_curve))
        self.assertTrue(callable(exponential_bonding_curve))
        self.assertTrue(callable(sigmoid_bonding_curve))
        self.assertTrue(callable(root_bonding_curve))
        self.assertTrue(callable(inverse_bonding_curve))

    def test_linear_bonding_curve(self):
        supply = np.array(1000, dtype=np.float32)
        result = linear_bonding_curve(supply, m=0.001, b=1)
        expected = 0.001 * 1000 + 1  # 2.0
        self.assertAlmostEqual(result, expected, places=4)

    def test_exponential_bonding_curve(self):
        supply = np.array(1000, dtype=np.float32)
        result = exponential_bonding_curve(supply, a=1, k=0.0005)
        expected = np.exp(0.0005 * 1000)  # exp(0.5)
        self.assertAlmostEqual(result, expected, places=4)

    def test_sigmoid_bonding_curve(self):
        # With S0 equal to supply, exp term becomes exp(0)=1, so value = K/2.
        supply = np.array(5000, dtype=np.float32)
        result = sigmoid_bonding_curve(supply, K=10, k=0.0001, S0=5000)
        self.assertAlmostEqual(result, 5.0, places=4)

    def test_root_bonding_curve(self):
        supply = np.array(1000, dtype=np.float32)
        result = root_bonding_curve(supply, k=0.1)
        expected = np.sqrt(1000) * 0.1
        self.assertAlmostEqual(result, expected, places=4)

    def test_inverse_bonding_curve(self):
        supply = np.array(1000, dtype=np.float32)
        result = inverse_bonding_curve(supply, k=100000)
        expected = 100000 / (1000 + 1)
        self.assertAlmostEqual(result, expected, places=4)

if __name__ == '__main__':
    unittest.main()
