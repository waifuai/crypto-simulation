import numpy as np
from config import INITIAL_TOKENS

# --- Data Generation ---
def generate_user_data(num_users, airdrop_strategy, user_params):
    initial_holdings = np.zeros(num_users)
    user_activity = np.random.poisson(lam=20.0, size=num_users).astype(np.float32)
    user_activity = user_activity + np.random.uniform(low=0, high=5, size=num_users)

    airdrop_amount = INITIAL_TOKENS * airdrop_strategy["percentage"]

    if airdrop_strategy["type"] == "none":
        eligibility = np.zeros(num_users)
    elif airdrop_strategy["type"] == "uniform":
        eligibility = np.ones(num_users)
    elif airdrop_strategy["type"] == "tiered":
        criteria_map = {
            'holdings': initial_holdings,
            'activity': user_activity
        }
        criteria_values = criteria_map.get(airdrop_strategy.get('criteria', 'none'), 0)

        # Vectorized threshold checks
        thresholds = np.array(airdrop_strategy.get('thresholds', []), dtype=np.float32)
        weights = np.array(airdrop_strategy.get('weights', []), dtype=np.float32)
        eligibility = (criteria_values[:, None] >= thresholds).dot(weights)


    elif airdrop_strategy["type"] == "lottery":
        num_winners = int(num_users * airdrop_strategy["winners_fraction"])
        winners = np.random.choice(num_users, size=num_winners, replace=False)
        eligibility = np.zeros(num_users)
        eligibility[winners] = 1
    else:
        eligibility = np.zeros(num_users)

    airdrop_distribution = np.where(
      eligibility > 0,
      airdrop_amount * eligibility / np.sum(eligibility),
      0.0
    )

    return airdrop_distribution, user_activity