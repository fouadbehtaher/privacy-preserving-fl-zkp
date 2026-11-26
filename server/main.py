"""FastAPI interface for the federated learning server.

Client updates are accepted only with a proof that passes server.zkp_verifier. Since no real
verifier exists yet, POST /submit_update rejects every update. Local/offline aggregation is
available only as a library call (server.aggregation), used by the tests.
"""
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from server.models import build_model, get_flat_params
from server.zkp_verifier import verify_training_proof

app = FastAPI(title="Privacy-preserving FL server (ZKP verification not implemented)")
_global_model = build_model()


class UpdateIn(BaseModel):
    client_id: str
    num_samples: int
    weights: List[float]
    proof: dict | None = None
    public_inputs: dict | None = None


@app.get("/health")
def health():
    return {"status": "ok", "zkp_verifier": "not_implemented"}


@app.get("/model")
def get_model():
    return {"weights": get_flat_params(_global_model).tolist()}


@app.post("/submit_update")
def submit_update(update: UpdateIn):
    if update.proof is None or not verify_training_proof(update.proof, update.public_inputs or {}):
        raise HTTPException(status_code=403, detail="update rejected: no valid training-integrity proof")
    # Reached only once a real verifier exists. Aggregation of verified updates is not wired in yet.
    raise HTTPException(status_code=501, detail="verified-update aggregation not implemented")
