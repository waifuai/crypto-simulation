import numpy as np
from constants import COMMISSION_DYNAMICS_STEP, DYNAMIC_ADJUSTMENT_RATE, MOVING_AVERAGE_WINDOW, INITIAL_COMMISSION_RATE
import logging
from typing import Dict, Any, List

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

class Affiliate:
    """
    Represents an affiliate in the system.
    """
    def __init__(self, affiliate_id: int, initial_commission_rate: float, is_whale: bool=False):
        """
        Initializes an affiliate.

        Args:
            affiliate_id (int): The ID of the affiliate.
            initial_commission_rate (float): The initial commission rate for the affiliate.
            is_whale (bool): Whether the affiliate is a whale (default: False).
        """
        self.affiliate_id: int = affiliate_id
        self.commission_rate: float = initial_commission_rate
        self.is_whale: bool = is_whale
        self.base_currency_balance: np.ndarray = np.array(1000.0, dtype=np.float32)
        self.wallet: Dict[str, Any] = {}
        self.total_referral_amount: np.ndarray = np.array(0.0, dtype=np.float32)
        self.total_earned: np.ndarray = np.array(0.0, dtype=np.float32)
        self.earnings_history: List[float] = []
        self.commission_rate_history: List[float] = []
        self.recent_investment: List[float] = []  # Track recent investment amounts
        self.whale_investment_capacity: float = np.random.uniform(5000, 10000) if is_whale else 0

    def adjust_commission_dynamically(self, step: int) -> None:
        """
        Adjusts the commission rate dynamically based on recent investment.

        Args:
            step (int): The current step in the simulation.
        """
        if step % COMMISSION_DYNAMICS_STEP == 0:
            avg_investment = np.mean(self.recent_investment) if self.recent_investment else 0
            if avg_investment > 50:  # Example threshold
                self.commission_rate += DYNAMIC_ADJUSTMENT_RATE
            else:
                self.commission_rate -= DYNAMIC_ADJUSTMENT_RATE
            self.commission_rate = max(0, min(self.commission_rate, 0.20)) # Cap commission rate
            logging.info(f"Affiliate {self.affiliate_id} commission rate adjusted to {self.commission_rate:.4f} based on avg investment {avg_investment:.2f}")

    def calculate_commission(self, trade_amount: float) -> float:
        """
        Calculates the commission earned on a trade.

        Args:
            trade_amount (float): The amount of the trade.

        Returns:
            float: The commission earned.
        """
        return trade_amount * self.commission_rate

    def track_referral(self, trade_amount: float) -> None:
        """
        Tracks a referral and updates the affiliate's earnings.

        Args:
            trade_amount (float): The amount of the trade.
        """
        commission_earned = self.calculate_commission(trade_amount)
        self.total_earned += np.array(commission_earned, dtype=np.float32)
        self.total_referral_amount += np.array(trade_amount, dtype=np.float32)
        logging.info(f"Affiliate {self.affiliate_id} earned commission: {commission_earned:.2f}")