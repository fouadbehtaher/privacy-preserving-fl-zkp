"""Weighted averaging of client model updates.

This is only the aggregation step. It does not check that an update is honest:
that is the job of the zero-knowledge proof, which is not implemented yet
(see server/zkp_verifier.py). Do not feed it unverified updates in a real deployment.
"""
import torch


def weighted_average(updates, weights):
    if not updates:
        raise ValueError("no updates to aggregate")
    if len(updates) != len(weights):
        raise ValueError("updates and weights must have the same length")
    if any(w <= 0 for w in weights):
        raise ValueError("weights must be positive")
    total = float(sum(weights))
    first = updates[0]
    out = torch.zeros_like(first)
    for u, w in zip(updates, weights):
        if u.shape != first.shape:
            raise ValueError("all updates must have the same shape")
        if not torch.isfinite(u).all():
            raise ValueError("update contains NaN or Inf")
        out += u * (w / total)
    return out
