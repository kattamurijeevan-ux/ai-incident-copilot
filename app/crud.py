from app.models import IncidentRecord


def save_incident(db, incident_id, timestamp, incident, rca_report, generated_logs):
    record = IncidentRecord(
        incident_id=incident_id,
        timestamp=timestamp,
        severity=incident["severity"],
        priority=incident["priority"],
        risk_score=incident["risk_score"],
        root_cause=rca_report["suspected_root_cause"],
        remediation=", ".join(rca_report["recommended_remediation_plan"]),
        raw_logs=generated_logs
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


def get_all_incidents(db):
    return db.query(IncidentRecord).order_by(
        IncidentRecord.timestamp.desc()
    ).all()