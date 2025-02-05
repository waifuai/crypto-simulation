import unittest
from simulation import token_simulation_step, affiliate_simulation_step, run_simulation

class TestSimulation(unittest.TestCase):

    def test_simulation_functions_exist(self):
        self.assertTrue(callable(token_simulation_step))
        self.assertTrue(callable(affiliate_simulation_step))
        self.assertTrue(callable(run_simulation))

    def test_run_simulation(self):
        token_histories, affiliate_histories = run_simulation()
        # Verify that for each token, histories contain non-empty lists.
        for token_name, histories in token_histories.items():
            self.assertTrue(len(histories["price"]) > 0)
            self.assertTrue(len(histories["supply"]) > 0)
            self.assertTrue(len(histories["bonding_curve"]) > 0)
        # Verify that for each affiliate, histories are populated.
        for aff_id, histories in affiliate_histories.items():
            self.assertTrue(len(histories["earned"]) > 0)
            self.assertTrue(len(histories["commission_rate"]) > 0)
            self.assertTrue(len(histories["wallet"]) > 0)
            self.assertTrue(len(histories["base_currency_balance"]) > 0)

if __name__ == '__main__':
    unittest.main()
