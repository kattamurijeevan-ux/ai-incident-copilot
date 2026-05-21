import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("data/incidents.json", "r") as f:
    incidents = json.load(f)

texts = [
    incident["symptoms"]
    for incident in incidents
]

embeddings = model.encode(texts)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings).astype("float32"))


def retrieve_similar_incidents(query, top_k=3):
    query_embedding = model.encode([query])

    distances, indices = index.search(
        np.array(query_embedding).astype("float32"),
        k=top_k
    )

    results = []

    for distance, idx in zip(distances[0], indices[0]):
        incident = incidents[idx]

        confidence = 1 / (1 + float(distance))

        results.append({
            "title": incident["title"],
            "symptoms": incident["symptoms"],
            "root_cause": incident["root_cause"],
            "fix": incident["fix"],
            "confidence": round(confidence, 3)
        })

    return results