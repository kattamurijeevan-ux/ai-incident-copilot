from fastapi import FastAPI
from pydantic import BaseModel

from app.log_parser import parse_logs
from app.detector import detect_incident
from app.llm_agent import generate_incident_report

app = FastAPI(title="AI Incident Copilot")


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