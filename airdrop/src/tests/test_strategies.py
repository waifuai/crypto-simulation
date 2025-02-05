import pytest
from strategies import generate_airdrop_strategies, AIRDROP_PARAMETER_GRID

def test_generate_airdrop_strategies():
    max_strategies = 3
    strategies = generate_airdrop_strategies(AIRDROP_PARAMETER_GRID, max_strategies)
    # Ensure we don’t generate more than max_strategies.
    assert len(strategies) <= max_strategies
    for strat in strategies:
        # Check that each strategy has a name and expected keys.
        assert "name" in strat
        assert "type" in strat
        # If the strategy is lottery, it should have a winners_fraction key.
        if strat["type"] == "lottery":
            assert "winners_fraction" in strat
