import numpy as np

# --- Bonding Curve Functions (Numpy Compatible) ---
def linear_bonding_curve(supply, m=0.001, b=1):
    return np.array(m, dtype=np.float32) * np.array(supply, dtype=np.float32) + np.array(b, dtype=np.float32)

def exponential_bonding_curve(supply, a=1, k=0.0005):
    return np.array(a, dtype=np.float32) * np.exp(np.array(k, dtype=np.float32) * np.array(supply, dtype=np.float32))

def sigmoid_bonding_curve(supply, K=10, k=0.0001, S0=5000):
    return np.array(K, dtype=np.float32) / (
        1
        + np.exp(
            -np.array(k, dtype=np.float32)
            * (np.array(supply, dtype=np.float32) - np.array(S0, dtype=np.float32))
        )
    )

def root_bonding_curve(supply, k=0.1):
    return np.sqrt(np.array(supply, dtype=np.float32)) * np.array(k, dtype=np.float32)

def inverse_bonding_curve(supply, k=100000):
    return np.array(k, dtype=np.float32) / (np.array(supply, dtype=np.float32) + 1)

bonding_curve_functions = [
    linear_bonding_curve,
    exponential_bonding_curve,
    sigmoid_bonding_curve,
    root_bonding_curve,
    inverse_bonding_curve,
]