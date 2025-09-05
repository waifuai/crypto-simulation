#!/usr/bin/env python3
"""
Example Scenario: Basic Multi-Protocol Simulation

This script demonstrates how to run multiple protocols in parallel
using the unified orchestrator.
"""

import sys
import os

# Add parent directory to path to import protocol wrappers
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from orchestrator import run_multi_protocol_simulation
from affiliate.notebook.main import AffiliateProtocolWrapper

# Temporarily disable some parameters for faster demo
NUM_SIMULATION_STEPS = 10  # Quick demo run

class SimpleDeFiProtocolWrapper:
    """Minimal DeFi wrapper for demonstration"""

    def __init__(self):
        self.tvl = 10000
        self.total_agents = 50  # Simplified

    def initialize(self):
        pass

    def run_step(self, step_num):
        # Simple growth simulation
        self.tvl *= 1.01  # 1% growth per step

    def export_state(self):
        return {
            'prices': {'DeFi_Token': 1.5},
            'supplies': {'DeFi_Token': self.tvl},
            'tvl': self.tvl
        }

    def accept_update(self, update):
        pass

    def get_final_results(self):
        return {
            'final_tvl': self.tvl,
            'total_agents': self.total_agents
        }

def main():
    """Run a sample multi-protocol scenario"""

    print("🚀 Starting Multi-Protocol Simulation Demo")
    print("=" * 50)

    # Initialize protocols
    protocols = {
        'affiliate': AffiliateProtocolWrapper(),
        'defi': SimpleDeFiProtocolWrapper()
    }

    # Run simulation
    num_steps = NUM_SIMULATION_STEPS
    results = run_multi_protocol_simulation(protocols, num_steps=num_steps)

    print("\n📊 Simulation Results:")
    print(f"  Steps: {num_steps}")

    print("\n--- Affiliate Protocol ---")
    aff_results = results['affiliate']
    print(f"  Final TVL: ${aff_results['total_tvl']:.2f}")
    print(f"  Avg Affiliate Balance: ${aff_results['avg_affiliate_balance']:.2f}")
    print(f"  Duration: {aff_results['duration']} steps")

    print("\n--- DeFi Protocol ---")
    defi_results = results['defi']
    print(f"  Final TVL: ${defi_results['final_tvl']:.2f}")
    print(f"  Total Agents: {defi_results['total_agents']}")

    print("\n--- Global Ecosystem ---")
    shared = results['global_state']
    print(f"  Total Global TVL: ${sum([shared['protocol_states'].get(p, {}).get('tvl', 0) for p in protocols]):.2f}")

    print("\n🎉 Multi-protocol simulation completed!")
    print("This demonstrates the basic integration framework.")
    print("Next steps: Add bridges, arbitrage, and more complex protocols.")

if __name__ == "__main__":
    main()