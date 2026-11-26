import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "sample_data"))

import pytest
import torch

from client.federated_client import FederatedClient
from sample_data import make_synthetic_client_data
from server.aggregation import weighted_average
from server.models import build_model, get_flat_params, set_flat_params


def test_flat_params_roundtrip():
    m1, m2 = build_model(), build_model()
    set_flat_params(m2, get_flat_params(m1))
    assert torch.equal(get_flat_params(m1), get_flat_params(m2))
    with pytest.raises(ValueError):
        set_flat_params(m2, get_flat_params(m1)[:-1])


def test_weighted_average_math():
    a, b = torch.zeros(4), torch.ones(4) * 4
    assert torch.allclose(weighted_average([a, b], [1, 3]), torch.ones(4) * 3)


def test_aggregation_rejects_bad_input():
    with pytest.raises(ValueError):
        weighted_average([], [])
    with pytest.raises(ValueError):
        weighted_average([torch.zeros(2), torch.zeros(3)], [1, 1])
    with pytest.raises(ValueError):
        weighted_average([torch.tensor([float("nan")])], [1])
    with pytest.raises(ValueError):
        weighted_average([torch.zeros(2)], [0])


def test_offline_rounds_reduce_loss_on_synthetic_data():
    torch.manual_seed(0)
    clients = [FederatedClient(f"c{i}", *make_synthetic_client_data(seed=i)) for i in range(3)]
    flat = get_flat_params(build_model())
    first = None
    for _ in range(15):
        ups = [c.local_update(flat, epochs=3) for c in clients]
        first = first if first is not None else sum(u["loss"] for u in ups) / 3
        flat = weighted_average([u["weights"] for u in ups], [u["num_samples"] for u in ups])
        last = sum(u["loss"] for u in ups) / 3
    assert last < first
