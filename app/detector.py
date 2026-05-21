def detect_incident(parsed_logs):
    error_count = sum(
        1 for log in parsed_logs
        if log["severity"] == "ERROR"
    )

    warn_count = sum(
        1 for log in parsed_logs
        if log["severity"] == "WARN"
    )

    if error_count >= 3:
        severity = "HIGH"
    elif error_count >= 1:
        severity = "MEDIUM"
    elif warn_count >= 2:
        severity = "LOW"
    else:
        severity = "NORMAL"

    return {
        "error_count": error_count,
        "warn_count": warn_count,
        "severity": severity
    }