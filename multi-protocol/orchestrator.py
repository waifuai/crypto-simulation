import numpy as np
import threading
import time
import random
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)

class SharedEcosystemState:
    """Manages global state across all protocols"""

    def __init__(self):
        self.global_price_market = {}  # token_id: price
        self.total_tvl = 0
        self.protocol_states = {}  # proto_id: state
        self.message_bus = []  # List of inter-protocol messages

    def update_global_prices(self, protocol_id, prices):
        """Update global prices from a protocol"""
        for token, price in prices.items():
            self.global_price_market[token] = price

    def get_global_price(self, token):
        return self.global_price_market.get(token, 1.0)  # Default price

class BridgeManager:
    """Manages bridges between protocols"""

    def __init__(self):
        self.bridges = {}  # (from_proto, to_proto): bridge_config
        self.pending_transfers = []  # List of (agent, from_proto, to_proto, amount, delay)

    def create_bridge(self, from_proto, to_proto, fee_rate=0.003, delay_steps=3, failure_prob=0.005):
        self.bridges[(from_proto, to_proto)] = {
            'fee_rate': fee_rate,
            'delay_steps': delay_steps,
            'failure_prob': failure_prob
        }

    def initiate_transfer(self, agent_id, from_proto, to_proto, amount):
        if (from_proto, to_proto) in self.bridges:
            config = self.bridges[(from_proto, to_proto)]
            transfer = {
                'agent_id': agent_id,
                'from_proto': from_proto,
                'to_proto': to_proto,
                'amount': amount,
                'remaining_delay': config['delay_steps'],
                'fee': amount * config['fee_rate'],
                'failed': random.random() < config['failure_prob']
            }
            self.pending_transfers.append(transfer)
            logging.debug(f"Transfer initiated: {agent_id} from {from_proto} to {to_proto}")

class ProtocolWrapper(threading.Thread):
    """Wrapper to run a protocol simulation in parallel"""

    def __init__(self, protocol_id, protocol_instance, shared_state, bridge_manager, num_steps):
        super().__init__()
        self.protocol_id = protocol_id
        self.protocol = protocol_instance
        self.shared_state = shared_state
        self.bridge_manager = bridge_manager
        self.num_steps = num_steps
        self.daemon = True
        self.results = {}

    def run(self):
        logging.info(f"Starting protocol {self.protocol_id}")

        # Initialize protocol
        self.protocol.initialize()

        for step in range(self.num_steps):
            # Export state to shared ecosystem
            state = self.protocol.export_state()
            self.shared_state.protocol_states[self.protocol_id] = state
            self.shared_state.update_global_prices(self.protocol_id, state.get('prices', {}))

            # Run simulation step
            self.protocol.run_step(step)

            # Handle incoming transfers
            for transfer in self.bridge_manager.pending_transfers:
                if transfer['to_proto'] == self.protocol_id and transfer['remaining_delay'] <= 0:
                    if not transfer['failed']:
                        self.protocol.accept_transfer(transfer)
                    self.bridge_manager.pending_transfers.remove(transfer)

        # Final results
        self.results = self.protocol.get_final_results()
        logging.info(f"Protocol {self.protocol_id} completed")

def run_multi_protocol_simulation(protocols_config, num_steps=100, num_shared_agents=50):
    """
    Main orchestrator function

    protocols_config: Dict of {'proto_id': protocol_instance}
    """
    shared_state = SharedEcosystemState()
    bridge_manager = BridgeManager()

    # Create shared agents pool
    shared_agents = [{'id': i, 'balance': 100, 'tokens': {}} for i in range(num_shared_agents)]

    # Initialize protocol wrappers
    wrappers = []
    for proto_id, proto_instance in protocols_config.items():
        wrapper = ProtocolWrapper(proto_id, proto_instance, shared_state, bridge_manager, num_steps)
        wrappers.append(wrapper)

    # Start bridges between protocols (example for Affiliate and DeFi)
    if 'affiliate' in protocols_config and 'defi' in protocols_config:
        bridge_manager.create_bridge('affiliate', 'defi', fee_rate=0.005, delay_steps=5)
        bridge_manager.create_bridge('defi', 'affiliate')

    logging.info("Starting simulation with protocols:", list(protocols_config.keys()))

    # Start all protocols
    for wrapper in wrappers:
        wrapper.start()

    # Run simulation steps
    for step in range(num_steps):
        # Sync shared state and handle bridges
        time.sleep(0.01)  # Simulate processing time

        # Process bridge transfers
        for transfer in bridge_manager.pending_transfers:
            transfer['remaining_delay'] -= 1

        if step % 10 == 0:
            logging.info(f"Step {step}/{num_steps}: Global TVL = {shared_state.total_tvl}")

    # Wait for completion
    for wrapper in wrappers:
        wrapper.join()

    # Aggregate results
    results = {'global_state': shared_state.__dict__}
    for wrapper in wrappers:
        results[wrapper.protocol_id] = wrapper.results

    logging.info("Multi-protocol simulation completed")
    return results

if __name__ == "__main__":
    """
    Example usage:
    from affiliate.notebook.main import run_simulation as affiliate_sim
    from defi.notebook.main import run_simulation as defi_sim

    protocols = {
        'affiliate': AffiliateProtocolWrapper(),
        'defi': DeFiProtocolWrapper()
    }

    results = run_multi_protocol_simulation(protocols, num_steps=50)
    print(results)
    """
    print("Run this script with actual protocol instances defined.")