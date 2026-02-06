# Perplexity-Style AI Agent (Built From Scratch)

## Overview

This project implements a **Perplexity-like AI assistant** that can intelligently decide whether to:

- Answer a user query using **internal model knowledge**, or  
- **Retrieve external information** from the web before answering.

The purpose of this project is **not** to build a polished chatbot UI or use agent frameworks, but to deeply understand how **real AI agents are structured internally**—with explicit decision-making, retrieval boundaries, and grounded responses.

Everything is built **from scratch**, without LangChain, LlamaIndex, or other abstraction-heavy frameworks.

---

## Core Idea

Most chatbots let an LLM silently decide everything.

This system does **not**.

Instead, it enforces a strict and inspectable pipeline:


Each step has a **single responsibility**, making the system debuggable, explainable, and safe.

User Query
↓
Query Classifier (decision only)
↓
Deterministic Orchestrator
↓
Optional Web Retrieval (raw evidence)
↓
Grounded Answer Generation

---

## Architecture Breakdown

### 1. Query Classifier (`classifier.py`)

The classifier is responsible only for **decision-making**.

It analyzes the user query and outputs a **structured JSON object** describing:

- Query type (procedural, factual, opinion, etc.)
- Time sensitivity
- Subjectivity
- Precision requirements
- Whether retrieval is required
- What the next action should be

**Important:**  
The classifier **never answers the question**.

#### Why this matters
- Decisions are explicit and logged
- Failures are inspectable
- The system commits to a plan before acting

This mirrors how real agent systems separate **planning** from **execution**.

---

### 2. Orchestrator (`orchestrator.py`)

The orchestrator is the **control layer** of the system.

It:
- Reads the classifier output
- Chooses the correct execution path
- Enforces clarification or refusal when needed
- Coordinates retrieval and generation

The orchestrator is **fully deterministic**.

> Only one component is “smart” at a time.

This is what keeps the system predictable and debuggable.

---

### 3. Retrieval Module (`retrieval.py`)

The retrieval module is intentionally **dumb and honest**.

It:
- Performs a web search
- Fetches raw page content
- Returns unprocessed evidence with source metadata

It explicitly **does not**:
- Summarize
- Decide relevance
- Rank truth
- Answer the question

#### Why retrieval does not summarize
Summarization is a reasoning step and introduces bias.  
Retrieval should surface **raw, messy reality**, including conflicts and uncertainty.

---

### 4. Answer Generator (`generator.py`)

There are two answer paths:

#### Internal Answer
Used when:
- The classifier decides retrieval is unnecessary
- The query is procedural or timeless

#### Grounded Answer
Used when:
- External evidence is retrieved
- The model is constrained to answer **only from sources**
- The model may **refuse** if evidence is insufficient

#### Why refusal is allowed
- Some questions demand impossible precision
- Some evidence is conflicting or outdated
- Correctness is prioritized over fluency

Refusal is treated as a **correct outcome**, not a failure.

---

## File Structure

perplexity_clone/
├── classifier.py # LLM-based query classification
├── retrieval.py # Web search and page fetching
├── generator.py # Internal vs grounded answer generation
├── orchestrator.py # Deterministic control logic
├── prompts.py # All prompts centralized
├── utils.py # LLM client and logging
├── main.py # CLI entry point
├── requirements.txt
└── .gitignore

Each file has a single, clearly defined responsibility.

---

## How to Run

### 1. Environment setup

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Add API key

OPENAI_API_KEY=your_api_key_here

### 3. Run the agent

python main.py

### 4. Few Examples

#### Example 1

Ask: who was the first president of india?

Output:
[CLASSIFIER] {'query_type': 'factual', 'time_sensitivity': 'timeless', 'subjectivity': 'objective', 'precision_required': 'low', 'retrieval_decision': 'no_retrieval', 'confidence_level': 'high', 'next_action': 'answer_directly'}
[GENERATOR] Using internal knowledge

ANSWER:
The first president of India was Dr. Rajendra Prasad. He served from 1950 to 1962.

#### Example 2

Ask: what is the best small cap mutual fund that i can buy right now?

Output:
[CLASSIFIER] {'query_type': 'comparative', 'time_sensitivity': 'time_sensitive', 'subjectivity': 'subjective', 'precision_required': 'high', 'retrieval_decision': 'retrieve', 'confidence_level': 'medium', 'next_action': 'perform_retrieval'}
[RETRIEVAL] Searching for: what is the best small cap mutual fund that i can buy right now

ANSWER:
I couldn’t find reliable sources for this.

#### Example 3

Ask: write me a sql query, where i need to the most purchased items in descending order

Output:
[CLASSIFIER] {'query_type': 'procedural', 'time_sensitivity': 'timeless', 'subjectivity': 'objective', 'precision_required': 'medium', 'retrieval_decision': 'no_retrieval', 'confidence_level': 'high', 'next_action': 'answer_directly'}
[GENERATOR] Using internal knowledge

ANSWER:
Certainly! Here’s a SQL query that retrieves the most purchased items in descending order based on the number of purchases. This assumes you have a table named `purchases` with a column `item_id` that identifies the items and a column `quantity` that indicates how many of each item was purchased.

```sql
SELECT item_id, SUM(quantity) AS total_purchased
FROM purchases
GROUP BY item_id
ORDER BY total_purchased DESC;
```

This query groups the purchases by `item_id`, sums the quantities for each item, and orders the results in descending order of total purchases. Adjust the table and column names as necessary to fit your database schema.

#### Example 4

Ask: Why OpenAI did not release the count of parameters that is being used in ChatGPT 5.2?

Output:
[CLASSIFIER] {'query_type': 'opinion', 'time_sensitivity': 'unknown', 'subjectivity': 'subjective', 'precision_required': 'medium', 'retrieval_decision': 'retrieve', 'confidence_level': 'medium', 'next_action': 'perform_retrieval'}
[RETRIEVAL] Searching for: Why OpenAI did not release the count of parameters that is being used in ChatGPT 5.2?

ANSWER:
I couldn’t find reliable sources for this.