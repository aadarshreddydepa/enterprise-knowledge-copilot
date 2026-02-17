from typing import List
import numpy as np


class InMemoryVectorClient:
    def __init__(self):
        self.vectors = []

    def upsert(self, items: List[dict]):
        self.vectors.extend(items)

    def search(self, query_vector: list[float], allowed_roles: list[str], top_k: int = 5):
        query = np.array(query_vector)
        scored = []

        for item in self.vectors:
            if not set(item["metadata"].get("roles", [])).intersection(allowed_roles):
                continue

            vec = np.array(item["values"])
            score = np.dot(query, vec) / (
                np.linalg.norm(query) * np.linalg.norm(vec)
            )
            scored.append((score, item))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in scored[:top_k]]


vector_client = InMemoryVectorClient()
