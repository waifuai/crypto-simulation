import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'affiliate/src')))
from affiliate import Affiliate

class TestAffiliate(unittest.TestCase):

    def test_affiliate_initialization(self):
        affiliate = Affiliate(affiliate_id=1, initial_commission_rate=0.05)
        self.assertEqual(affiliate.affiliate_id, 1)
        self.assertEqual(affiliate.commission_rate, 0.05)
    def test_calculate_commission(self):
        affiliate = Affiliate(affiliate_id=1, initial_commission_rate=0.1)
        commission = affiliate.calculate_commission(trade_amount=1000)
        self.assertEqual(commission, 100)

    def test_track_referral(self):
        affiliate = Affiliate(affiliate_id=1, initial_commission_rate=0.1)
        affiliate.track_referral(trade_amount=500)
        self.assertEqual(affiliate.total_referral_amount, 500)
        affiliate.track_referral(trade_amount=250)
        self.assertEqual(affiliate.total_referral_amount, 750)
        self.assertFalse(affiliate.is_whale)

if __name__ == '__main__':
    unittest.main()