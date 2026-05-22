from datetime import datetime
import uuid
import random

from fastapi import FastAPI
from pydantic import BaseModel

from app.log_parser import parse_logs
from app.detector import detect_incident
from app.llm_agent import generate_incident_report
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Incident Copilot")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LogRequest(BaseModel):
    logs: str


@app.get("/")
def home():
    return {
        "message": "AI Incident Copilot is running"
    }


@app.post("/analyze")
def analyze_logs(request: LogRequest):

    parsed_logs = parse_logs(request.logs)

    incident = detect_incident(parsed_logs)

    report = generate_incident_report(
        parsed_logs,
        incident
    )

    return {
        "parsed_logs": parsed_logs,
        "incident": incident,
        "report": report
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AI Incident Copilot"
    }

@app.get("/simulate")
def simulate_logs():

    sample_logs = [
        "ERROR PaymentService timeout calling Stripe API",
        "WARN Database connection pool near limit",
        "ERROR AuthService token validation failed",
        "INFO User login successful",
        "ERROR InventoryService failed to update stock",
        "WARN High API latency detected",
        "ERROR Kafka consumer disconnected",
        "INFO Scheduled backup completed"
    ]

    generated_logs = "\n".join(
        random.choice(sample_logs)
        for _ in range(5)
    )

    parsed_logs = parse_logs(generated_logs)

    incident = detect_incident(parsed_logs)

    report = generate_incident_report(
        parsed_logs,
        incident
    )
    
    return {
    "incident_id": str(uuid.uuid4()),
    "timestamp": datetime.utcnow().isoformat(),
    "generated_logs": generated_logs,
    "incident": incident,
    "report": report
}