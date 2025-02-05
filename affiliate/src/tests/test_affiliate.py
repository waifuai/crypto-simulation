import unittest
import numpy as np
from affiliate import Affiliate
from constants import COMMISSION_DYNAMICS_STEP, DYNAMIC_ADJUSTMENT_RATE

class TestAffiliate(unittest.TestCase):

    def test_affiliate_initialization(self):
        affiliate = Affiliate(affiliate_id=1, initial_commission_rate=0.05)
        self.assertEqual(affiliate.affiliate_id, 1)
        self.assertEqual(affiliate.commission_rate, 0.05)
        self.assertFalse(affiliate.is_whale)

    def test_calculate_commission(self):
        affiliate = Affiliate(affiliate_id=1, initial_commission_rate=0.1)
        commission = affiliate.calculate_commission(trade_amount=1000)
        self.assertEqual(commission, 100)

    def test_track_referral(self):
        affiliate = Affiliate(affiliate_id=1, initial_commission_rate=0.1)
        affiliate.track_referral(trade_amount=500)
        self.assertAlmostEqual(affiliate.total_referral_amount, 500)
        affiliate.track_referral(trade_amount=250)
        self.assertAlmostEqual(affiliate.total_referral_amount, 750)

    def test_adjust_commission_dynamically_increase(self):
        # Test that commission_rate increases when average investment > 50.
        affiliate = Affiliate(affiliate_id=2, initial_commission_rate=0.1)
        affiliate.recent_investment = [100, 100, 100]  # average > 50
        step = COMMISSION_DYNAMICS_STEP  # step divisible by dynamics step
        affiliate.adjust_commission_dynamically(step)
        self.assertAlmostEqual(affiliate.commission_rate, 0.1 + DYNAMIC_ADJUSTMENT_RATE)

    def test_adjust_commission_dynamically_decrease(self):
        # Test that commission_rate decreases when average investment <= 50.
        affiliate = Affiliate(affiliate_id=3, initial_commission_rate=0.1)
        affiliate.recent_investment = [10, 10, 10]  # average below threshold
        step = COMMISSION_DYNAMICS_STEP
        affiliate.adjust_commission_dynamically(step)
        self.assertAlmostEqual(affiliate.commission_rate, 0.1 - DYNAMIC_ADJUSTMENT_RATE)

if __name__ == '__main__':
    unittest.main()
