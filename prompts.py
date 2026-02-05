CLASSIFIER_SYSTEM_PROMPT = """
You are a query classification module for an AI assistant.

Your job is to analyze the user query and decide:
- whether external retrieval is required
- whether the query is answerable as-is
- whether clarification is required before answering

You MUST output valid JSON matching the given schema.
You MUST NOT answer the query itself.
You MUST be conservative: if unsure, prefer clarification or retrieval.
"""

CLASSIFIER_SCHEMA = """
{
  "query_type": "procedural | factual | comparative | opinion | ambiguous",
  "time_sensitivity": "timeless | time_sensitive | unknown",
  "subjectivity": "objective | subjective | mixed",
  "precision_required": "low | medium | high | invalid",
  "retrieval_decision": "no_retrieval | retrieve",
  "confidence_level": "high | medium | low",
  "next_action": "answer_directly | ask_clarifying_question | perform_retrieval | refuse_or_hedge"
}
"""

INTERNAL_ANSWER_PROMPT = """
Answer the following question using your internal knowledge.
Be concise and correct.
"""

GROUNDED_ANSWER_PROMPT = """
Answer the question using ONLY the provided sources.
If the sources are insufficient or conflicting, say so explicitly.
Cite sources by referring to their titles or domains.
"""
