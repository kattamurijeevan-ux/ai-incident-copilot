# AI Incident Copilot

An AI-powered incident analysis and retrieval system built using FastAPI, vector embeddings, and semantic search.

## Features

- Log parsing and severity detection
- Incident classification engine
- Semantic similarity retrieval using embeddings
- Confidence-scored historical incident matching
- REST API using FastAPI
- RAG-style incident intelligence workflow-
- Simulated production log generation
- Risk scoring and priority assignment
- Unique incident IDs and timestamps
- Top-3 similar incident retrieval with confidence scores

---

# Architecture

Logs
↓
Parser
↓
Incident Detector
↓
Embedding Generator
↓
Vector Search
↓
Historical Incident Retrieval
↓
Recommended Fix

---

# Tech Stack

- Python
- FastAPI
- Sentence Transformers
- FAISS
- NumPy
- Pydantic

---

# API Endpoints

## Analyze Logs

POST `/analyze`

Example request:

```json
{
  "logs": "ERROR PaymentService timeout"
}
```

---

## Health Check

GET `/health`

---

# Example Output

```json
{
  "severity": "MEDIUM",
  "most_likely_root_cause": "Third-party payment provider latency",
  "recommended_fix": "Add exponential backoff and retry queue"
}
```

---

# Run Locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

# Future Improvements

- Kafka-based real-time log streaming
- OpenAI-powered root cause analysis
- LangGraph multi-agent workflows
- Grafana dashboards
- Docker/Kubernetes deployment
- ML-based anomaly detection