import pytest
from unittest.mock import patch
import numpy as np
from optimization import evaluate_parameters, optimize_bonding_curve
from config import INITIAL_TOKEN_SUPPLY, NUM_AGENTS

@patch('optimization.simulation_step')
def test_evaluate_parameters(mock_simulation_step):
    # Mock simulation_step to return predictable values
    mock_simulation_step.return_value = (None, None, None, 10)  # Constant price

    params = {'type': 'linear', 'm': 0.1, 'b': 1.0}
    score = evaluate_parameters(params, num_runs=2)
    # With a constant price, std dev should be 0, so the score should be based on price_change
    assert score == 1000.0

    mock_simulation_step.return_value = (None, None, None, 15)
    score = evaluate_parameters(params, num_runs=1)
    assert score == 1000.0

@patch('optimization.evaluate_parameters')
def test_optimize_bonding_curve(mock_evaluate_parameters):
    mock_evaluate_parameters.return_value = 1.0  # Mock a good score

    # Test linear curve optimization
    best_params = optimize_bonding_curve('linear', n_trials=2)
    assert best_params['type'] == 'linear'
    assert 'm' in best_params
    assert 'b' in best_params

    # Test exponential curve optimization
    best_params = optimize_bonding_curve('exponential', n_trials=2)
    assert best_params['type'] == 'exponential'
    assert 'a' in best_params
    assert 'k' in best_params

    # Test sigmoid curve optimization
    best_params = optimize_bonding_curve('sigmoid', n_trials=2)
    assert best_params['type'] == 'sigmoid'
    assert 'k' in best_params
    assert 's0' in best_params
    assert 'k_max' in best_params

     # Test multi-segment curve optimization
    best_params = optimize_bonding_curve('multi-segment', n_trials=2)
    assert best_params['type'] == 'multi-segment'
    assert 'breakpoint' in best_params
    assert 'm' in best_params
    assert 'a' in best_params
    assert 'k' in best_params

    # Test invalid curve type
    with pytest.raises(ValueError):
        optimize_bonding_curve('invalid', n_trials=2)