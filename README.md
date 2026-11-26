# Privacy-Preserving Federated Learning with Zero-Knowledge Proofs

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![PyTorch](https://img.shields.io/badge/PyTorch-2.1-red)
![ZKP](https://img.shields.io/badge/ZKP-Groth16-orange)

A secure and privacy-preserving federated learning system enhanced with Zero-Knowledge Proofs for collaborative threat detection without sharing raw data.

## Current status

Implemented and tested offline (synthetic data only, Python 3.11, CPU torch, no network service): a small PyTorch model, local client training, weighted averaging of updates, and a FastAPI app (`/health`, `/model`, `/submit_update`). `pytest tests` passes (8 tests) after `pip install -r requirements.txt`.

**The server still rejects every update.** `server/zkp_verifier.py` is not connected to any proof system, so `/submit_update` returns 403 (the verifier is NOT IMPLEMENTED, not a cryptographic check). A separate Groth16 prototype exists but is not wired into the server:

- `zkp-circuits/training_integrity.circom` proves, for public initial weights `w0` and final weights `wT`, that `wT` is the result of T epochs of full-batch gradient descent of an integer fixed-point **linear regression** (`pred = floor(w.x / 2^K)`, `err = pred - y`, `w <- w - floor(sum(err*x) / 2^M)`) on private data `(x, y)`. The exact statement and bounds are in the file header.
- `client/zk_training.py` is a Python trainer that matches the circuit exactly; a test checks that the circuit's public output equals it.
- `zkp-utils/` builds the circuit, makes a proof and verifies it (`npm ci` in `zkp-circuits/`, then `pytest tests/test_zkp_groth16.py`). The 6 tests (toy size: T=2, N=4, F=3) check an honest proof, a changed final or initial weight, a mismatched proof, out-of-range data (no proof) and a garbage proof. Last run: 6 passed.
- **Limits:** the trusted setup is generated locally for testing and must not be trusted. There is no dataset commitment, so the proof does not say which dataset was used (that design is undecided). It is linear regression, not a neural network or logistic regression. Full size (T=3, N=1000, F=100) was not built: compiling it did not finish in 100 s here, and my rough estimate is a few million constraints, which is unmeasured. Secure aggregation, poisoning protection and client authentication are not implemented.

## 🚀 Features

- **Federated Learning**: Train ML models without centralizing data
- **Zero-Knowledge Proofs**: Verify training integrity without revealing secrets
- **Secure Aggregation**: Protect model updates with encryption
- **Threat Detection**: Collaborative cybersecurity threat detection
- **Production Ready**: Dockerized and scalable architecture

## 🏗️ Architecture
┌─────────────┐ ┌──────────────┐ ┌─────────────┐
│ Clients │ │ Server │ │ Dashboard │
│ │ │ │ │ │
│ • Local │ │ • ZKP │ │ • Monitor │
│ Training │◄──►│ Verification│◄──►│ System │
│ • ZKP Proof │ │ • Secure │ │ • Metrics │
│ Generation│ │ Aggregation│ │ │
└─────────────┘ └──────────────┘ └─────────────┘


Docker Deployment

docker-compose up --build

🛠️ Usage
Start the Server
cd server
uvicorn main:app --host 0.0.0.0 --port 8000

Access Dashboard
Open http://localhost:8000/docs for API documentation

🔧 Configuration
Server Configuration
Edit server/config.py:

python
SERVER_CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "model_input_size": 100,
    "model_output_size": 2
}
ZKP Circuit Parameters
Edit zkp-circuits/circuit_params.json:

json
{
    "nFeatures": 100,
    "nSamples": 1000,
    "nEpochs": 3
}
🧪 Testing
Run the test suite:

bash
pytest tests/ -v
Performance testing:

bash
python tests/performance_test.py

📊 Results

<img width="541" height="283" alt="image" src="https://github.com/user-attachments/assets/87cb252f-3df6-4fe4-877c-4e86af6abfae" />

🔒 Security Features
✅ Zero-Knowledge Proofs for integrity verification

✅ Secure multi-party computation

✅ Encrypted model updates

✅ Client authentication and authorization

✅ Protection against model poisoning attacks

📚 Documentation
API Documentation

Deployment Guide

Theoretical Background

Circuit Design

🤝 Contributing
Fork the repository

Create a feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request





