"""Small PyTorch model shared by clients and server (sizes follow the README: 100 inputs, 2 outputs)."""
import torch
from torch import nn


def build_model(input_size=100, output_size=2):
    return nn.Sequential(nn.Linear(input_size, 32), nn.ReLU(), nn.Linear(32, output_size))


def get_flat_params(model):
    return torch.cat([p.detach().reshape(-1) for p in model.parameters()]).clone()


def set_flat_params(model, flat):
    if flat.numel() != sum(p.numel() for p in model.parameters()):
        raise ValueError("flat parameter vector has the wrong length for this model")
    offset = 0
    with torch.no_grad():
        for p in model.parameters():
            n = p.numel()
            p.copy_(flat[offset:offset + n].reshape(p.shape))
            offset += n
