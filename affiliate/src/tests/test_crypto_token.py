import unittest
import numpy as np
from crypto_token import Token
from bonding_curves import linear_bonding_curve

class TestCryptoToken(unittest.TestCase):

    def test_token_initialization(self):
        token = Token(name="TestToken", initial_supply=1000, initial_price=1, bonding_curve_func=linear_bonding_curve)
        self.assertEqual(token.name, "TestToken")
        self.assertEqual(token.supply, 1000)
        self.assertEqual(token.price, 1)
        self.assertEqual(token.bonding_curve_func, linear_bonding_curve)

    def test_token_buy(self):
        token = Token(name="TestToken", initial_supply=1000, initial_price=1, bonding_curve_func=linear_bonding_curve)
        old_supply = token.supply
        old_price = token.price
        buy_amount = np.array(100, dtype=np.float32)
        # Buy tokens: fees and burn reduce effective amount.
        new_price = token.buy(buy_amount)
        fee = 100 * token.transaction_fee_rate
        burn = 100 * token.burn_rate
        effective_amount = 100 - fee - burn
        expected_supply = old_supply + effective_amount
        self.assertAlmostEqual(token.supply, expected_supply, places=4)
        expected_price = linear_bonding_curve(np.array(expected_supply, dtype=np.float32))
        self.assertAlmostEqual(token.price, expected_price, places=4)

    def test_token_sell(self):
        token = Token(name="TestToken", initial_supply=1000, initial_price=1, bonding_curve_func=linear_bonding_curve)
        # Simulate a buy to change supply.
        token.buy(np.array(100, dtype=np.float32))
        old_supply = token.supply
        sell_amount = np.array(50, dtype=np.float32)
        new_price = token.sell(sell_amount)
        fee = 50 * token.transaction_fee_rate
        burn = 50 * token.burn_rate
        effective_amount = 50 - fee - burn
        expected_supply = old_supply - effective_amount
        self.assertAlmostEqual(token.supply, expected_supply, places=4)
        expected_price = linear_bonding_curve(np.array(expected_supply, dtype=np.float32))
        self.assertAlmostEqual(token.price, expected_price, places=4)

    def test_change_bonding_curve(self):
        token = Token(name="TestToken", initial_supply=1000, initial_price=1, bonding_curve_func=linear_bonding_curve)
        current_func = token.bonding_curve_func
        token.change_bonding_curve()
        self.assertNotEqual(token.bonding_curve_func, current_func)

    def test_change_bonding_curve_parameters(self):
        token = Token(name="TestToken", initial_supply=1000, initial_price=1, bonding_curve_func=linear_bonding_curve)
        token.change_bonding_curve_parameters()
        # After changing parameters, the metadata should reflect a dynamic parameter change.
        self.assertEqual(token.curve_metadata.get("function_name"), "linear_bonding_curve")

if __name__ == '__main__':
    unittest.main()
