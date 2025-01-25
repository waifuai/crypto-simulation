import logging

# print("Experimentation module is running")
import numpy as np
from simulation import run_simulation

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Parameter Experimentation ---
logging.info("Starting parameter experimentation...")

param_ranges = {
    'price_elasticity': np.linspace(0.01, 0.1, 10),
    'resource_regen_rate': np.linspace(0.005, 0.02, 10),
    'tax_rate': np.linspace(0.0, 0.05, 10),
    'agent_expense_rate': np.linspace(0.1, 0.5, 10)
}

experiment_results = {}

for param_name, param_values in param_ranges.items():
    # logging.info(f"Experimenting with {param_name}...")
    experiment_results[param_name] = []
    for value in param_values:
        params = {param_name: value}
        # logging.info(f"Running simulation with {param_name} = {value}")
        results = run_simulation(params)
        results['param_value'] = value
        experiment_results[param_name].append(results)

# --- Visualize Results ---
# --- Visualize Results ---
# --- Further Analysis (Example) ---
logging.info("Performing further analysis...")

if 'tax_rate' in experiment_results:
    tax_results = experiment_results['tax_rate']
    best_tax_rate_data = min(tax_results, key=lambda x: x['num_bankruptcies'])
    logging.info(f"Tax rate that minimizes bankruptcies: {best_tax_rate_data['param_value']}")

if 'resource_regen_rate' in experiment_results:
    regen_results = experiment_results['resource_regen_rate']
    best_regen_rate_data = max(regen_results, key=lambda x: x['avg_final_balance'])
    logging.info(f"Regen rate that maximizes average final balance: {best_regen_rate_data['param_value']}")

logging.info("Experimentation and analysis complete.")