from classifier import classify_query
from retrieval import retrieve
from generator import generate_internal_answer, generate_grounded_answer
from utils import llm_chat, log

def answer_user(user_query):
    classification = classify_query(llm_chat, user_query)
    log("CLASSIFIER", classification)

    action = classification["next_action"]

    if action == "ask_clarifying_question":
        return "Can you clarify your criteria before I answer?"

    if action == "refuse_or_hedge":
        return "I can't give a precise answer to this as stated."

    if classification["retrieval_decision"] == "no_retrieval":
        return generate_internal_answer(user_query)

    search_query = user_query  # v1: direct pass-through
    retrieval_result = retrieve(search_query)

    if not retrieval_result["results"]:
        return "I couldn't find reliable sources for this."

    return generate_grounded_answer(user_query, retrieval_result)
