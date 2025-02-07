import numpy as np
from typing import Callable, List

# --- Bonding Curve Functions (Numpy Compatible) ---
def linear_bonding_curve(supply: np.ndarray, m: float=0.001, b: float=1) -> np.ndarray:
    """
    Calculates the price using a linear bonding curve.

    Args:
        supply (np.ndarray): The current supply.
        m (float): The slope of the line.
        b (float): The y-intercept of the line.

    Returns:
        np.ndarray: The price.
    """
    return np.array(m, dtype=np.float32) * np.array(supply, dtype=np.float32) + np.array(b, dtype=np.float32)

def exponential_bonding_curve(supply: np.ndarray, a: float=1, k: float=0.0005) -> np.ndarray:
    """
    Calculates the price using an exponential bonding curve.

    Args:
        supply (np.ndarray): The current supply.
        a (float): The scaling factor.
        k (float): The exponent coefficient.

    Returns:
        np.ndarray: The price.
    """
    return np.array(a, dtype=np.float32) * np.exp(np.array(k, dtype=np.float32) * np.array(supply, dtype=np.float32))

def sigmoid_bonding_curve(supply: np.ndarray, K: float=10, k: float=0.0001, S0: float=5000) -> np.ndarray:
    """
    Calculates the price using a sigmoid bonding curve.

    Args:
        supply (np.ndarray): The current supply.
        K (float): The maximum price.
        k (float): The steepness of the curve.
        S0 (float): The supply at the midpoint of the curve.

    Returns:
        np.ndarray: The price.
    """
    return np.array(K, dtype=np.float32) / (
        1
        + np.exp(
            -np.array(k, dtype=np.float32)
            * (np.array(supply, dtype=np.float32) - np.array(S0, dtype=np.float32))
        )
    )

def root_bonding_curve(supply: np.ndarray, k: float=0.1) -> np.ndarray:
    """
    Calculates the price using a root bonding curve.

    Args:
        supply (np.ndarray): The current supply.
        k (float): The scaling factor.

    Returns:
        np.ndarray: The price.
    """
    return np.sqrt(np.array(supply, dtype=np.float32)) * np.array(k, dtype=np.float32)

def inverse_bonding_curve(supply: np.ndarray, k: float=100000) -> np.ndarray:
    """
    Calculates the price using an inverse bonding curve.

    Args:
        supply (np.ndarray): The current supply.
        k (float): The scaling factor.

    Returns:
        np.ndarray: The price.
    """
    return np.array(k, dtype=np.float32) / (np.array(supply, dtype=np.float32) + 1)

bonding_curve_functions: List[Callable[[np.ndarray, float, float], np.ndarray]] = [
    linear_bonding_curve,
    exponential_bonding_curve,
    sigmoid_bonding_curve,
    root_bonding_curve,
    inverse_bonding_curve,
]