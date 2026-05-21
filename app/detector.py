def detect_incident(parsed_logs):

    error_count = sum(
        1 for log in parsed_logs
        if log["severity"] == "ERROR"
    )

    warn_count = sum(
        1 for log in parsed_logs
        if log["severity"] == "WARN"
    )

    risk_score = (error_count * 25) + (warn_count * 10)

    if risk_score >= 80:
        severity = "CRITICAL"
        priority = "P1"

    elif risk_score >= 50:
        severity = "HIGH"
        priority = "P2"

    elif risk_score >= 20:
        severity = "MEDIUM"
        priority = "P3"

    elif risk_score >= 10:
        severity = "LOW"
        priority = "P4"

    else:
        severity = "NORMAL"
        priority = "P5"

    return {
        "error_count": error_count,
        "warn_count": warn_count,
        "risk_score": risk_score,
        "severity": severity,
        "priority": priority
    }