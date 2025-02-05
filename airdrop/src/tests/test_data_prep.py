import pytest
import numpy as np
from data_prep import assign_user_parameters

def test_assign_user_parameters():
    num_users = 50
    params = assign_user_parameters(num_users)
    assert params.shape[0] == num_users
    # Check that each parameter is within [0, 1] after clipping.
    assert (params >= 0.0).all() and (params <= 1.0).all()
