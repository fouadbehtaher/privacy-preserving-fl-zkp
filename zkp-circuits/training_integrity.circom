pragma circom 2.0.0;
include "circomlib/circuits/bitify.circom";

// Statement (integer fixed-point linear regression, full-batch gradient descent):
//
//   Public : w0[F] (initial weights), wT[F] (final weights), and the template parameters T,N,F,K,M.
//   Private: x[N][F], y[N] (the training data).
//   Claim  : wT is what T epochs of the update below produce from w0 on (x, y), with
//            floor(v / 2^s) meaning exact integer floor division:
//     pred_i  = floor( (sum_j w_j * x_ij) / 2^K )
//     err_i   = pred_i - y_i
//     g_j     = sum_i err_i * x_ij
//     w_j    <- w_j - floor( g_j / 2^M )
//
// Values are integers (real value * 2^K). x, y and every w must lie in [-2^(BX-1), 2^(BX-1)).
// An honest prover whose intermediate values exceed the bit bounds B1/B2 gets no proof.
//
// NOT proved: that (x, y) is any particular dataset (no dataset commitment: undecided),
// that the weights came from a neural network, or anything about secure aggregation.

// out = floor(v / 2^S) for v in [-2^(B-1), 2^(B-1)); fails otherwise.
template FloorShift(B, S) {
    signal input v;
    signal output out;
    signal t;
    signal q;
    signal r;
    t <== v + (1 << (B - 1));
    q <-- t >> S;
    r <-- t & ((1 << S) - 1);
    t === q * (1 << S) + r;
    component rb = Num2Bits(S);
    rb.in <== r;
    component qb = Num2Bits(B - S);
    qb.in <== q;
    out <== q - (1 << (B - 1 - S));
}

// Proves v in [-2^(BX-1), 2^(BX-1)).
template Range(BX) {
    signal input v;
    component b = Num2Bits(BX);
    b.in <== v + (1 << (BX - 1));
}

template TrainingIntegrity(T, N, F, K, M, BX, B1, B2) {
    signal input w0[F];
    signal input x[N][F];
    signal input y[N];
    signal output wT[F];

    signal w[T + 1][F];
    signal dot[T][N][F + 1];
    signal pm[T][N][F];
    signal err[T][N];
    signal gacc[T][F][N + 1];
    signal gm[T][F][N];

    component rx[N][F];
    component ry[N];
    component rw[T + 1][F];
    component fp[T][N];
    component fg[T][F];

    for (var i = 0; i < N; i++) {
        ry[i] = Range(BX);
        ry[i].v <== y[i];
        for (var j = 0; j < F; j++) {
            rx[i][j] = Range(BX);
            rx[i][j].v <== x[i][j];
        }
    }
    for (var j = 0; j < F; j++) { w[0][j] <== w0[j]; }

    for (var e = 0; e < T; e++) {
        for (var j = 0; j < F; j++) {
            rw[e][j] = Range(BX);
            rw[e][j].v <== w[e][j];
        }
        for (var i = 0; i < N; i++) {
            dot[e][i][0] <== 0;
            for (var j = 0; j < F; j++) {
                pm[e][i][j] <== w[e][j] * x[i][j];
                dot[e][i][j + 1] <== dot[e][i][j] + pm[e][i][j];
            }
            fp[e][i] = FloorShift(B1, K);
            fp[e][i].v <== dot[e][i][F];
            err[e][i] <== fp[e][i].out - y[i];
        }
        for (var j = 0; j < F; j++) {
            gacc[e][j][0] <== 0;
            for (var i = 0; i < N; i++) {
                gm[e][j][i] <== err[e][i] * x[i][j];
                gacc[e][j][i + 1] <== gacc[e][j][i] + gm[e][j][i];
            }
            fg[e][j] = FloorShift(B2, M);
            fg[e][j].v <== gacc[e][j][N];
            w[e + 1][j] <== w[e][j] - fg[e][j].out;
        }
    }
    for (var j = 0; j < F; j++) {
        rw[T][j] = Range(BX);
        rw[T][j].v <== w[T][j];
        wT[j] <== w[T][j];
    }
}
