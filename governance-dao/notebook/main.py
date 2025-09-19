"""
DAO Governance Simulation and Voting Mechanism Analysis

This file implements a comprehensive simulation framework for analyzing different
Decentralized Autonomous Organization (DAO) governance mechanisms and voting systems.

Key Features:
1. Multiple Voting Mechanisms:
   - Simple token-weighted voting
   - Quadratic voting for more democratic outcomes
   - Delegation-based voting for scalability

2. Voter Behavior Modeling:
   - Different voter archetypes based on token holdings
   - Whale vs retail participant dynamics
   - Participation rate modeling and engagement analysis

3. Proposal System:
   - Dynamic proposal generation across different systems (MCP, bonding curves, etc.)
   - Parameter adjustment and fund allocation proposals
   - Treasury management and fund allocation tracking

4. Comprehensive Analytics:
   - Voter participation analysis and turnout metrics
   - Wealth inequality measurement (Gini coefficient)
   - Proposal success rates and voting power distribution
   - Cross-mechanism comparison and effectiveness analysis

The simulation integrates with external protocol data (affiliate systems) to create
realistic governance scenarios and analyzes how different voting mechanisms affect
DAO decision-making quality and participant engagement.
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
from typing import List, Dict
import os

# Configuration
NUM_VOTERS = 100
SIMULATION_STEPS = 50
TREASURY_INITIAL = 10000
PROPOSAL_SUBMISSION_RATE = 0.1
MIN_VOTING_THRESHOLD = 0.5
VOTER_PARTICIPATION_RATE = 0.8
WHALE_THRESHOLD_MULTIPLIER = 1.2  # Token holdings multiplier for "whales"

# Voting mechanisms
VOTING_MECHANISMS = ['simple', 'quadratic', 'delegation']

class Voter:
    def __init__(self, voter_id: int, token_holdings: float, is_whale: bool = False):
        self.id = voter_id
        self.token_holdings = token_holdings
        self.is_whale = is_whale
        self.voting_power_simple = token_holdings
        self.voting_power_quadratic = np.sqrt(token_holdings)
        self.participates = random.random() < VOTER_PARTICIPATION_RATE
        self.delegated_to = None

    def vote(self, proposal, voting_mechanism: str) -> float:
        if not self.participates:
            return 0

        # Base support probability depends on holdings and whale status
        support_chance = 0.5 + (0.2 if self.is_whale else 0)
        if self.token_holdings > np.mean([v.token_holdings for v in [self]]):  # Simplified, assume context
            support_chance += 0.1

        support = random.random() < support_chance

        if voting_mechanism == 'simple':
            vote_power = self.voting_power_simple if support else -self.voting_power_simple
        elif voting_mechanism == 'quadratic':
            vote_power = self.voting_power_quadratic if support else -self.voting_power_quadratic
        elif voting_mechanism == 'delegation':
            # Use delegated voting if applicable (simplified)
            delegate = self.delegated_to
            if delegate:
                vote_power = delegate.voting_power_simple if support else -delegate.voting_power_simple
            else:
                vote_power = self.voting_power_simple if support else -self.voting_power_simple
        else:
            vote_power = 0

        return vote_power

class Proposal:
    def __init__(self, proposal_id: int, proposer: Voter, change_type: str, target_system: str, change_value: float):
        self.id = proposal_id
        self.proposer = proposer
        self.change_type = change_type  # e.g., 'parameter', 'allocation'
        self.target_system = target_system  # e.g., 'mcp', 'bonding_curve'
        self.change_value = change_value
        self.votes = 0
        self.total_voting_power = 0
        self.pass_threshold = MIN_VOTING_THRESHOLD

    def cast_vote(self, voter: Voter, voting_mechanism: str):
        vote_power = voter.vote(self, voting_mechanism)
        self.votes += vote_power
        self.total_voting_power += abs(vote_power)

        # Special handling for whales insisting on certain proposals
        if voter.is_whale and self.change_type == 'parameter':
            self.votes += vote_power * 0.5  # Amplification for whale votes

    def is_passed(self) -> bool:
        if self.total_voting_power == 0:
            return False
        support_ratio = self.votes / self.total_voting_power
        return support_ratio > self.pass_threshold

class Treasury:
    def __init__(self, initial_funds: float):
        self.funds = initial_funds
        self.allocation_history = []

    def allocate_funds(self, amount: float, proposal: Proposal) -> bool:
        if self.funds >= amount:
            self.funds -= amount
            self.allocation_history.append((proposal.id, amount))
            return True
        return False

    def receive_fees(self, amount: float):
        self.funds += amount

    def get_total_allocated(self) -> float:
        return sum(amount for _, amount in self.allocation_history)

class Simulation:
    def __init__(self, num_voters: int, voting_mechanism: str):
        self.num_voters = num_voters
        self.voting_mechanism = voting_mechanism
        self.voters: List[Voter] = []
        self.proposals: List[Proposal] = []
        self.treasury = Treasury(TREASURY_INITIAL)
        self.proposal_count = 0
        self.metrics_history = []

        # Load data from other simulations
        self.load_external_data()

    def load_external_data(self):
        # Simplified: Load token holdings from affiliate simulation
        affiliate_output_path = os.path.join('..', 'affiliate', 'output.txt')
        try:
            with open(affiliate_output_path, 'r') as f:
                content = f.read()
            # Parse final balances or holdings (simplified parsing)
            lines = content.split('\n')
            holdings = []
            for line in lines:
                if 'Final Base Currency:' in line:
                    # Extract holding values (simplified)
                    holdings.append(float(line.split(':')[1].strip()))

            if holdings:
                median_holdings = np.median(holdings)
                whale_threshold = median_holdings * WHALE_THRESHOLD_MULTIPLIER
                for i in range(self.num_voters):
                    full_holdings = holdings[i % len(holdings)] if holdings else 100
                    is_whale = full_holdings > whale_threshold
                    self.voters.append(Voter(i, full_holdings, is_whale))

                # Handle delegation randomly for delegation mechanism
                if self.voting_mechanism == 'delegation':
                    for voter in self.voters:
                        if random.random() < 0.3:  # 30% delegation rate
                            voter.delegated_to = random.choice([v for v in self.voters if v.id != voter.id])
            else:
                # Fallback if no data
                for i in range(self.num_voters):
                    holdings = np.random.normal(100, 20)
                    is_whale = holdings > 120
                    self.voters.append(Voter(i, holdings, is_whale))
        except FileNotFoundError:
            print(f"Warning: {affiliate_output_path} not found. Using synthetic data.")
            for i in range(self.num_voters):
                holdings = np.random.normal(100, 20)
                is_whale = holdings > 120
                self.voters.append(Voter(i, holdings, is_whale))

    def generate_proposal(self) -> Proposal:
        proposer = random.choice(self.voters)
        change_type = random.choice(['parameter', 'allocation'])
        target_system = random.choice(['mcp', 'bonding_curve', 'affiliate', 'airdrop'])
        change_value = random.uniform(-0.1, 0.1)  # Parameter adjustment or allocation percentage

        self.proposal_count += 1
        return Proposal(self.proposal_count, proposer, change_type, target_system, change_value)

    def run_step(self, step: int):
        # Generate proposal
        if random.random() < PROPOSAL_SUBMISSION_RATE:
            proposal = self.generate_proposal()
            self.proposals.append(proposal)

            # Voting
            for voter in self.voters:
                proposal.cast_vote(voter, self.voting_mechanism)

            # Check if passed and execute
            if proposal.is_passed():
                if proposal.change_type == 'allocation':
                    amount = self.treasury.funds * abs(proposal.change_value)
                    self.treasury.allocate_funds(amount, proposal)
                    self.treasury.receive_fees(amount * 0.01)  # Small fee income

        # Record metrics
        participation_rate = sum(1 for v in self.voters if v.participates) / len(self.voters)
        active_proposals = len([p for p in self.proposals if not p.is_passed()])
        metrics = {
            'step': step,
            'participation_rate': participation_rate,
            'active_proposals': active_proposals,
            'treasury_funds': self.treasury.funds,
            'gini_coefficient': self.calculate_gini(),
            'passed_proposals': len([p for p in self.proposals if p.is_passed()]),
        }
        self.metrics_history.append(metrics)

    def calculate_gini(self) -> float:
        holdings = [v.token_holdings for v in self.voters]
        if not holdings:
            return 0
        holdings.sort()
        n = len(holdings)
        numerator = sum((2 * i - n - 1) * holding for i, holding in enumerate(holdings))
        denominator = n * sum(holdings)
        return numerator / denominator if denominator > 0 else 0

    def run_simulation(self) -> Dict:
        for step in range(SIMULATION_STEPS):
            self.run_step(step)

        # Compile results
        metrics_df = pd.DataFrame(self.metrics_history)
        final_metrics = {
            'total_participation': np.mean([m['participation_rate'] for m in self.metrics_history]),
            'passed_proposals_count': len([p for p in self.proposals if p.is_passed()]),
            'final_treasury': self.treasury.funds,
            'final_gini': self.metrics_history[-1]['gini_coefficient'],
            'voting_mechanism': self.voting_mechanism,
            'whale_influence': sum(1 for v in self.voters if v.is_whale) / len(self.voters),
            'metrics_history': metrics_df.to_dict('records')
        }
        return final_metrics

# Main execution
def main():
    results = []
    for voting_mechanism in VOTING_MECHANISMS:
        print(f"Running simulation with {voting_mechanism} voting...")
        sim = Simulation(NUM_VOTERS, voting_mechanism)
        result = sim.run_simulation()
        results.append(result)

        print(f"  Total Participation: {result['total_participation']:.2%}")
        print(f"  Passed Proposals: {result['passed_proposals_count']}")
        print(f"  Final Gini Coefficient: {result['final_gini']:.4f}")
        print(f"  Final Treasury Funds: ${result['final_treasury']:.2f}")
        print(f"  Whale Influence: {result['whale_influence']:.2%}")
        print("-" * 50)

    # Cross-mechanism comparison
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    mechanisms = [r['voting_mechanism'] for r in results]

    axes[0, 0].bar(mechanisms, [r['total_participation'] for r in results])
    axes[0, 0].set_title('Average Voter Participation')
    axes[0, 0].set_ylabel('Participation Rate')

    axes[0, 1].bar(mechanisms, [r['passed_proposals_count'] for r in results])
    axes[0, 1].set_title('Total Passed Proposals')

    axes[1, 0].bar(mechanisms, [r['final_gini'] for r in results])
    axes[1, 0].set_title('Final Gini Coefficient')
    axes[1, 0].set_ylabel('Gini Index')

    axes[1, 1].bar(mechanisms, [r['final_treasury'] for r in results])
    axes[1, 1].set_title('Final Treasury Funds')
    axes[1, 1].set_ylabel('Funds ($)')

    plt.tight_layout()
    plt.savefig('../output.png')
    plt.show()

    print("\nSimulation complete. Results saved to governance-dao/output.png")

if __name__ == "__main__":
    main()