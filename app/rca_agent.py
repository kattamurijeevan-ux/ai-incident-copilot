def build_incident_timeline(parsed_logs):
    timeline = []

    for index, log in enumerate(parsed_logs, start=1):
        timeline.append({
            "step": index,
            "severity": log["severity"],
            "event": log["message"]
        })

    return timeline


def identify_impacted_services(parsed_logs):
    services = []

    known_services = [
        "PaymentService",
        "AuthService",
        "InventoryService",
        "Database",
        "Kafka",
        "Redis",
        "API"
    ]

    for log in parsed_logs:
        for service in known_services:
            if service in log["message"]:
                services.append(service)

    return list(set(services))


def generate_rca_report(parsed_logs, incident, similar_incidents):
    timeline = build_incident_timeline(parsed_logs)
    impacted_services = identify_impacted_services(parsed_logs)

    best_match = similar_incidents[0]

    return {
        "incident_priority": incident["priority"],
        "risk_score": incident["risk_score"],
        "impacted_services": impacted_services,
        "timeline": timeline,
        "suspected_root_cause": best_match["root_cause"],
        "recommended_remediation_plan": [
            best_match["fix"],
            "Validate service health metrics",
            "Check recent deployments",
            "Monitor incident after remediation"
        ],
        "confidence": best_match["confidence"]
    }