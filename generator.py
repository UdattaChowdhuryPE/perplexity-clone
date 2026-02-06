from prompts import INTERNAL_ANSWER_PROMPT, GROUNDED_ANSWER_PROMPT
from utils import llm_chat, log

def generate_internal_answer(user_query):
    log("GENERATOR", "Using internal knowledge")
    messages = [
        {"role": "system", "content": INTERNAL_ANSWER_PROMPT},
        {"role": "user", "content": user_query}
    ]
    return llm_chat(messages)


def generate_grounded_answer(user_query, retrieval_result):
    log("GENERATOR", "Using retrieved evidence")

    sources_text = ""
    for r in retrieval_result["results"]:
        sources_text += f"\nSOURCE: {r['source']}\nTITLE: {r['title']}\nCONTENT:\n{r['content']}\n"

    messages = [
        {"role": "system", "content": GROUNDED_ANSWER_PROMPT},
        {"role": "user", "content": f"Question:\n{user_query}\n\nSources:\n{sources_text}"}
    ]

    return llm_chat(messages)
