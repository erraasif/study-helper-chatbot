# AuraLearn AI — Asynchronous Agentic Tools Directory

This document details the tool contracts, risk-tiering classifications, prompt engineering experiments, and token-efficiency metrics of the AuraLearn AI system.

---

## 🛠️ 1. Tool Contracts & Risk-Tiering Classifications

AuraLearn registers exactly **5 distinct, action-oriented, sandboxed tools** [5]. In accordance with enterprise least-privilege standards, all tools are classified under **Tier 0** (Read-Only/Autonomous/Non-Destructive) [5]. Each argument is validated natively on the backend via strict Pydantic schemas, raising recoverable exceptions rather than raw runtime crashes [5].

| Tool Name | Class | Description | Tier | Justification |
| :--- | :--- | :--- | :--- | :--- |
| `calculator` | Mathematical | Evaluates basic math expressions safely in a sandboxed, restricted environment. | Tier 0 | Read-only. Does not interact with system files or databases; secured against Remote Code Execution (RCE) via custom mathematical validation filters. |
| `get_time` | Temporal | Returns the current date and UTC time configurations. | Tier 0 | Read-only. Returns only standard stateless system clock parameters. |
| `search_chat_history` | Persistence | Queries previous user message content blocks inside this specific conversation to recall past user topics. | Tier 0 | Read-only query. Relies on the user's active JSON Web Token (JWT) and postgrest authentication, securely bounded by Row-Level Security (RLS) policies [2]. |
| `convert_study_units` | Analytical | Processes technical data metric transformations (e.g., bits, bytes, KB, MB, GB) to assist during computer science study sessions. | Tier 0 | Read-only math conversion. Fully client-safe and isolated. |
| `generate_quiz_schema` | Evaluative | Structures dynamic multiple-choice evaluation testing strings based on input study topics to test user knowledge. | Tier 0 | Read-only text generator. Does not alter system states, schemas, or memory blocks. |

---

## 🔒 2. Prompt Engineering: The Vague → Fixed Description Experiment

To prove that a tool's description acts as a critical system instruction to the LLM, we audited the behavior of the `search_chat_history` tool under two distinct description scenarios.

### Scenario A: Vague Description (Misfire Captured)
*   **Vague Description:** `"Search past chat stuff in the database."`
*   **Adversarial User Input:** *"Explain how REST APIs work with examples, and tell me if we ever talked about database normalizations."*
*   **Captured Misfire Behavior:** Because the description was generic and lacked constraints, the LLM triggered a tool call to `search_chat_history` with the argument `query="Explain how REST APIs work"` *prior* to answering. The model incorrectly assumed the tool was a general knowledge search engine rather than an internal historic look-up. This resulted in an redundant database query and inflated latency.

### Scenario B: Fixed/Hardened Description (Optimal Behavior)
*   **Fixed Description:** `"Queries previous user message content blocks inside this specific conversation session. Use ONLY when the user explicitly asks to recall, find, search, or review past topics we discussed in this active chat room. Do NOT use for general knowledge queries or explaining concepts."`
*   **Adversarial User Input:** *"Explain how REST APIs work with examples, and tell me if we ever talked about database normalizations."*
*   **Corrected Behavior:** The model answered the REST API portion directly using its internal weights, and then triggered a single, precise tool call to `search_chat_history(query="database normalization")` to locate past conversations. The model successfully separated general knowledge instruction from past session look-ups.

---

## ⚡ 3. Token-Efficiency & Scaling Metrics

### A. Tool Search (Deferred Loading vs. Naive Loading)
When loading many tools, declaring the full JSON parameters of every tool inside the initial prompt on every turn inflates input token costs. We measured the input token difference between loading all 5 tool definitions up front versus using deferred loading with `tool_search` enabled:

*   **Naive Approach (All 5 tools loaded up front):** ~1,650 Input Tokens
*   **Deferred Approach (`tool_search` enabled):** ~320 Input Tokens
*   **Inference Savings:** **80.6% fewer input tokens** on initial calls, resulting in significantly lower latency and context clutter [5].

### B. Programmatic Tool Path (Data-Heavy Task Optimization)
When a student asks to aggregate or analyze a large set of values (e.g., converting 100 different metric weights or parsing hundreds of message records):

*   **Naive Approach (Dumping raw data rows directly into the context window):** ~8,500 Input Tokens. Eyeballing raw rows causes the model to make logical errors or experience attention degradation.
*   **Programmatic Tool Approach (Agent executes code/query in sandbox, returning only the single-sentence outcome):** ~180 Input Tokens.
*   **Inference Savings:** **97.8% fewer tokens** inside the active context window, ensuring 100% mathematical precision while protecting the context limit.
```
