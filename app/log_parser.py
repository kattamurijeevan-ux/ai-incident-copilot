def parse_logs(raw_logs: str):
    lines = raw_logs.strip().split("\n")

    parsed_logs = []

    for line in lines:
        severity = "INFO"

        if "ERROR" in line:
            severity = "ERROR"
        elif "WARN" in line:
            severity = "WARN"

        parsed_logs.append({
            "severity": severity,
            "message": line
        })

    return parsed_logs