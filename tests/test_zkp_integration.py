"""The ZKP verifier is not implemented: these tests pin the fail-closed behaviour.
They do NOT test proof generation or verification, which do not exist yet."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient

from server.main import app
from server.zkp_verifier import verify_training_proof

client = TestClient(app)
BODY = {"client_id": "c0", "num_samples": 10, "weights": [0.0]}


def test_verifier_rejects_everything():
    assert verify_training_proof({"anything": 1}, {}) is False
    assert verify_training_proof({}, {}) is False


def test_health_reports_verifier_not_implemented():
    r = client.get("/health")
    assert r.status_code == 200 and r.json()["zkp_verifier"] == "not_implemented"


def test_update_without_proof_is_rejected():
    assert client.post("/submit_update", json=BODY).status_code == 403


def test_update_with_a_made_up_proof_is_rejected():
    r = client.post("/submit_update", json={**BODY, "proof": {"pi_a": [1]}, "public_inputs": {"x": 1}})
    assert r.status_code == 403
