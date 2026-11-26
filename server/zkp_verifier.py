"""Verification of the zero-knowledge proof of training integrity.

NOT IMPLEMENTED. The Groth16 circuit (zkp-circuits/) and a real verifier do not exist yet,
and the statement the proof must establish has not been decided by the project owner.
Until a real verifier is wired in, every proof is rejected (fail closed). There is no
accept-all mode, and nothing here claims that any training was verified.
"""


class VerifierNotConfigured(Exception):
    """Raised when a proof check is requested but no real verifier exists."""


def verify_training_proof(proof, public_inputs):
    """Return True only if a real verifier accepts the proof. Currently always rejects."""
    return False
