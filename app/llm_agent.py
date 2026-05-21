from app.retriever import retrieve_similar_incidents


def generate_incident_report(parsed_logs, incident):

    logs_text = "\n".join(
        log["message"]
        for log in parsed_logs
    )

    similar_incidents = retrieve_similar_incidents(
        logs_text,
        top_k=3
    )

    best_match = similar_incidents[0]

    return {
        "analysis": {
            "summary": "Potential production incident detected.",
            "severity": incident["severity"],
            "most_likely_root_cause": best_match["root_cause"],
            "recommended_fix": best_match["fix"],
            "similar_incidents": similar_incidents
        }
    }