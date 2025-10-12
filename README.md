# Privacy-Preserving Federated Learning with Zero-Knowledge Proofs

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![PyTorch](https://img.shields.io/badge/PyTorch-2.1-red)
![ZKP](https://img.shields.io/badge/ZKP-Groth16-orange)

A secure and privacy-preserving federated learning system enhanced with Zero-Knowledge Proofs for collaborative threat detection without sharing raw data.

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





