"""Synthetic data for offline tests. This is NOT real threat data."""
import numpy as np


def make_synthetic_client_data(n_samples=200, n_features=100, seed=0):
    """Two-class data: class 1 has a shifted mean on the first 10 features."""
    rng = np.random.default_rng(seed)
    y = rng.integers(0, 2, size=n_samples)
    x = rng.normal(0.0, 1.0, size=(n_samples, n_features)).astype("float32")
    x[y == 1, :10] += 1.5
    return x, y.astype("int64")
