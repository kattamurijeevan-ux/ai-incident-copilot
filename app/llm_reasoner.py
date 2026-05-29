import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_llm_reasoning(generated_logs, incident, rca_report):
    prompt = f"""
You are an expert AI incident response engineer.

Analyze this production incident.

Logs:
{generated_logs}

Incident metadata:
{incident}

RCA report:
{rca_report}

Return a concise incident reasoning report with:
1. What happened
2. Likely root cause
3. Business impact
4. Recommended engineering actions
5. Prevention plan
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert SRE and AI incident response engineer."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content