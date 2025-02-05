import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'affiliate/src')))
from crypto_token import Token
from bonding_curves import linear_bonding_curve

class TestCryptoToken(unittest.TestCase):

    def test_token_initialization(self):
        token = Token(name="TestToken", initial_supply=1000, initial_price=1, bonding_curve_func=linear_bonding_curve)
        self.assertEqual(token.name, "TestToken")
        self.assertEqual(token.supply, 1000)
        self.assertEqual(token.price, 1)
        self.assertEqual(token.bonding_curve_func, linear_bonding_curve)

if __name__ == '__main__':
    unittest.main()