"""Local training on a client's own data (PyTorch)."""
import torch
from torch import nn

from server.models import build_model, get_flat_params, set_flat_params


def train_local(global_flat, x, y, epochs=3, lr=0.05, input_size=100, output_size=2):
    """Start from the global weights, train on local data, return (new flat weights, n_samples, final loss)."""
    model = build_model(input_size, output_size)
    set_flat_params(model, global_flat)
    xt, yt = torch.as_tensor(x), torch.as_tensor(y)
    opt = torch.optim.SGD(model.parameters(), lr=lr)
    loss_fn = nn.CrossEntropyLoss()
    loss = None
    for _ in range(epochs):
        opt.zero_grad()
        loss = loss_fn(model(xt), yt)
        loss.backward()
        opt.step()
    return get_flat_params(model), len(y), float(loss)
