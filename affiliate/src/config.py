import argparse
import logging
from constants import NUM_SIMULATION_STEPS, NUM_TOKENS, NUM_AFFILIATES, INITIAL_SUPPLY, INITIAL_PRICE, INITIAL_COMMISSION_RATE, INITIAL_TOKEN_INVESTMENT, bonding_curve_change_intervals, BONDING_CURVE_PARAM_CHANGE_INTERVAL

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Simulate a token economy.")
    parser.add_argument(
        "--num_simulation_steps", type=int, default=100, help="Number of simulation steps."
    )
    parser.add_argument(
        "--num_tokens", type=int, default=5, help="Number of tokens to simulate."
    )
    parser.add_argument(
        "--num_affiliates", type=int, default=5, help="Number of affiliates."
    )
    parser.add_argument(
        "--initial_supply", type=int, default=10000, help="Initial token supply."
    )
    parser.add_argument(
        "--initial_price", type=float, default=1.0, help="Initial token price."
    )
    parser.add_argument(
        "--initial_commission_rate",
        type=float,
        default=0.10,
        help="Initial affiliate commission rate.",
    )
    return parser.parse_args()

args = parse_arguments()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

NUM_SIMULATION_STEPS = args.num_simulation_steps
NUM_TOKENS = args.num_tokens
NUM_AFFILIATES = args.num_affiliates
INITIAL_SUPPLY = args.initial_supply
INITIAL_PRICE = args.initial_price
INITIAL_COMMISSION_RATE = args.initial_commission_rate