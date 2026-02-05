import json
from prompts import CLASSIFIER_SYSTEM_PROMPT, CLASSIFIER_SCHEMA

def classify_query(llm_client, user_query: str) -> dict:
    messages = [
        {"role": "system", "content": CLASSIFIER_SYSTEM_PROMPT},
        {"role": "user", "content": f"Schema:\n{CLASSIFIER_SCHEMA}\n\nUser Query:\n{user_query}"}
    ]

    response = llm_client(messages)

    try:
        classification = json.loads(response)
    except json.JSONDecodeError:
        raise ValueError("Classifier did not return valid JSON")

    return classification
