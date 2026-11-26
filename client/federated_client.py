"""Federated client. Offline only for now: it trains locally and returns the update.

It does not generate a zero-knowledge proof (the circuit does not exist yet), so an update from
this client is rejected by the server's /submit_update.
"""
from client.model_training import train_local


class FederatedClient:
    def __init__(self, client_id, x, y):
        self.client_id, self.x, self.y = client_id, x, y

    def local_update(self, global_flat, epochs=3, lr=0.05):
        flat, n, loss = train_local(global_flat, self.x, self.y, epochs=epochs, lr=lr)
        return {"client_id": self.client_id, "num_samples": n, "weights": flat, "loss": loss, "proof": None}
