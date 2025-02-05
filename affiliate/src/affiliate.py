import numpy as np
from constants import COMMISSION_DYNAMICS_STEP, DYNAMIC_ADJUSTMENT_RATE, MOVING_AVERAGE_WINDOW, INITIAL_COMMISSION_RATE

class Affiliate:
    def __init__(self, affiliate_id, initial_commission_rate, is_whale=False):
        self.affiliate_id = affiliate_id
        self.commission_rate = initial_commission_rate
        self.is_whale = is_whale
        self.base_currency_balance = np.array(1000.0, dtype=np.float32)
        self.wallet = {}
        self.total_referral_amount = np.array(0.0, dtype=np.float32)
        self.total_earned = np.array(0.0, dtype=np.float32)
        self.earnings_history = []
        self.commission_rate_history = []
        self.recent_investment = []  # Track recent investment amounts
        self.whale_investment_capacity = np.random.uniform(5000, 10000) if is_whale else 0

    def adjust_commission_dynamically(self, step):
        if step % COMMISSION_DYNAMICS_STEP == 0:
            avg_investment = np.mean(self.recent_investment) if self.recent_investment else 0
            if avg_investment > 50:  # Example threshold
                self.commission_rate += DYNAMIC_ADJUSTMENT_RATE
            else:
                self.commission_rate -= DYNAMIC_ADJUSTMENT_RATE
            self.commission_rate = max(0, min(self.commission_rate, 0.20)) # Cap commission rate
            logging.info(f"Affiliate {self.affiliate_id} commission rate adjusted to {self.commission_rate:.4f} based on avg investment {avg_investment:.2f}")

    def calculate_commission(self, trade_amount):
        return trade_amount * self.commission_rate

    def track_referral(self, trade_amount):
        commission_earned = self.calculate_commission(trade_amount)
        self.total_earned += np.array(commission_earned, dtype=np.float32)
        self.total_referral_amount += np.array(trade_amount, dtype=np.float32)
        logging.info(f"Affiliate {self.affiliate_id} earned commission: {commission_earned:.2f}")

import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)