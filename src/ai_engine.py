import os
from groq import Groq

def analyze_with_ai(alerts):
    """
    Sends flagged alerts to Groq for SOC summary and remediation.
    """
    groq_api_key = os.environ.get("GROQ_API_KEY")
    if not groq_api_key:
        return "AI Analysis unavailable: GROQ_API_KEY not found."

    client = Groq(
        api_key=groq_api_key,
    )

    if not alerts:
        return "No security alerts to analyze."

    # Convert alerts to a string format suitable for the prompt
    alerts_str = "\n".join([str(alert) for alert in alerts])

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Act as a Senior SOC Analyst. Summarize these security alerts, explain the potential impact, and suggest a mitigation step."
            },
            {
                "role": "user",
                "content": f"Security Alerts: {alerts_str}"
            }
        ],
        model="llama-3.1-8b-instant",
    )

    return chat_completion.choices[0].message.content
