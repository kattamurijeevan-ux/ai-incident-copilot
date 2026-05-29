from app.database import SessionLocal
from app.crud import save_incident, get_all_incidents
from app.rca_agent import generate_rca_report
from app.postmortem_agent import generate_postmortem
from datetime import datetime
from app.llm_reasoner import generate_llm_reasoning
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
@app.get("/simulate-rca")
def simulate_rca():

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
        for _ in range(6)
    )

    parsed_logs = parse_logs(generated_logs)
    incident = detect_incident(parsed_logs)
    report = generate_incident_report(parsed_logs, incident)

    similar_incidents = report["analysis"]["similar_incidents"]

    rca_report = generate_rca_report(
        parsed_logs,
        incident,
        similar_incidents
    )

    incident_id = str(uuid.uuid4())
    timestamp = datetime.utcnow()

    db = SessionLocal()

    save_incident(
        db,
        incident_id,
        timestamp,
        incident,
        rca_report,
        generated_logs
    )

    db.close()

    return {
        "incident_id": incident_id,
        "timestamp": timestamp.isoformat(),
        "generated_logs": generated_logs,
        "incident": incident,
        "rca_report": rca_report
    }


@app.get("/simulate-postmortem")
def simulate_postmortem():

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
        for _ in range(6)
    )

    parsed_logs = parse_logs(generated_logs)
    incident = detect_incident(parsed_logs)
    report = generate_incident_report(parsed_logs, incident)

    similar_incidents = report["analysis"]["similar_incidents"]

    rca_report = generate_rca_report(
        parsed_logs,
        incident,
        similar_incidents
    )

    incident_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()

    postmortem = generate_postmortem(
        incident_id,
        timestamp,
        generated_logs,
        incident,
        rca_report
    )

    return postmortem

@app.get("/simulate-llm-reasoning")
def simulate_llm_reasoning():

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
        for _ in range(6)
    )

    parsed_logs = parse_logs(generated_logs)
    incident = detect_incident(parsed_logs)
    report = generate_incident_report(parsed_logs, incident)

    similar_incidents = report["analysis"]["similar_incidents"]

    rca_report = generate_rca_report(
        parsed_logs,
        incident,
        similar_incidents
    )

    llm_reasoning = generate_llm_reasoning(
        generated_logs,
        incident,
        rca_report
    )

    return {
        "incident_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "generated_logs": generated_logs,
        "incident": incident,
        "rca_report": rca_report,
        "llm_reasoning": llm_reasoning
    }
@app.get("/incidents")
def list_incidents():
    db = SessionLocal()
    records = get_all_incidents(db)
    db.close()

    return [
        {
            "incident_id": record.incident_id,
            "timestamp": record.timestamp.isoformat(),
            "severity": record.severity,
            "priority": record.priority,
            "risk_score": record.risk_score,
            "root_cause": record.root_cause,
            "remediation": record.remediation
        }
        for record in records
    ]