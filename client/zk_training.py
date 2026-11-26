"""Integer fixed-point linear-regression trainer that exactly matches the statement in
zkp-circuits/training_integrity.circom. Pure Python, no dependencies.

All values are integers (real value * 2**k). Python's >> is floor division, as in the circuit.
"""


def train_int(w0, x, y, epochs, k, m):
    """T epochs of full-batch gradient descent. Returns the final integer weights."""
    f = len(w0)
    w = list(w0)
    for _ in range(epochs):
        err = []
        for xi, yi in zip(x, y):
            pred = sum(wj * xj for wj, xj in zip(w, xi)) >> k
            err.append(pred - yi)
        w = [w[j] - (sum(e * xi[j] for e, xi in zip(err, x)) >> m) for j in range(f)]
    return w


def required_bits(n, f, bx, k):
    """Bit bounds (B1, B2) that are safe for inputs in [-2**(bx-1), 2**(bx-1))."""
    lim = 2 ** (bx - 1)
    dot_max = f * lim * lim
    b1 = dot_max.bit_length() + 2
    err_max = (dot_max >> k) + 1 + lim
    g_max = n * err_max * lim
    b2 = g_max.bit_length() + 2
    return b1, b2
