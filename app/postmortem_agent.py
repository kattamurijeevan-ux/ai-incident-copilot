def generate_postmortem(incident_id, timestamp, generated_logs, incident, rca_report):

    return {
        "postmortem_title": f"Postmortem Report - {incident['severity']} Incident",
        "incident_id": incident_id,
        "created_at": timestamp,
        "severity": incident["severity"],
        "priority": incident["priority"],
        "risk_score": incident["risk_score"],

        "executive_summary": (
            f"A {incident['severity']} incident was detected with "
            f"{incident['error_count']} errors and {incident['warn_count']} warnings. "
            f"The suspected root cause is: {rca_report['suspected_root_cause']}."
        ),

        "impact": {
            "impacted_services": rca_report["impacted_services"],
            "customer_impact": "Potential service degradation or failed user transactions.",
            "business_impact": "Possible delay in request processing and operational response."
        },

        "timeline": rca_report["timeline"],

        "root_cause": rca_report["suspected_root_cause"],

        "remediation_steps": rca_report["recommended_remediation_plan"],

        "prevention_actions": [
            "Add automated alerts for recurring error patterns",
            "Improve service-level monitoring dashboards",
            "Review retry and timeout configurations",
            "Create runbooks for similar future incidents"
        ],

        "raw_logs": generated_logs
    }