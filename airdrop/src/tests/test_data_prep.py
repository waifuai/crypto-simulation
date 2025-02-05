import pytest
import numpy as np
from data_prep import scale_data, normalize_data

def test_scale_data():
    data = np.array([1, 2, 3, 4, 5])
    scaled_data = scale_data(data, 0, 10)
    assert np.allclose(scaled_data, np.array([0, 2.5, 5, 7.5, 10]))

def test_normalize_data():
    data = np.array([1, 2, 3, 4, 5])
    normalized_data = normalize_data(data)
    assert np.allclose(normalized_data, np.array([-1.4142, -0.7071, 0, 0.7071, 1.4142]), atol=1e-4)