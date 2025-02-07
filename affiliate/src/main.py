from simulation import run_simulation
from config import NUM_TOKENS
import pandas as pd
from typing import Dict, Any, Tuple

if __name__ == "__main__":
    """Runs the simulation and prints a summary of the results."""
    token_histories, affiliate_histories = run_simulation()

    summary: Dict[str, Dict[str, Any]] = {
        "tokens": {},
        "affiliates": {}
    }

    for token_name, histories in token_histories.items():
        summary["tokens"][token_name] = {
            "final_price": histories["price"][-1] if histories["price"] else 0,
            "final_supply": histories["supply"][-1] if histories["supply"] else 0,
            "final_bonding_curve": histories["bonding_curve"][-1] if histories["bonding_curve"] else None
        }
    
    for aff_id, histories in affiliate_histories.items():
        summary["affiliates"][aff_id] = {
            "final_earned": histories["earned"][-1] if histories["earned"] else 0,
            "final_commission_rate": histories["commission_rate"][-1] if histories["commission_rate"] else 0,
            "final_base_currency": histories["base_currency_balance"][-1] if histories["base_currency_balance"] else 0,
            "final_wallet": histories["wallet"][-1] if histories["wallet"] else {}
        }

    print("\n--- Token Summary ---")
    for token_name, metrics in summary["tokens"].items():
        print(f"\nToken: {token_name}")
        print(f"  Final Price: {metrics['final_price']:.2f}")
        print(f"  Final Supply: {metrics['final_supply']:.2f}")
        print(f"  Final Bonding Curve: {metrics['final_bonding_curve']}")

    print("\n--- Affiliate Summary ---")
    for aff_id, metrics in summary["affiliates"].items():
        print(f"\nAffiliate: {aff_id}")
        print(f"  Final Base Currency: {metrics['final_base_currency']:.2f}")
        print(f"  Final Commission Rate: {metrics['final_commission_rate']:.4f}")