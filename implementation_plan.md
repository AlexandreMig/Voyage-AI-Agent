# Implementation Plan - Phase 2: Build & Coding

This document details the technical implementation plan for developing the core logic, memory, safety, and evaluation elements of **VoyageAI**.

---

## Proposed Changes

### 1. Custom Travel Planning Tools

We will create a new Python module [tools.py](file:///Users/alexlopes/.gemini/antigravity/scratch/voyageai/app/tools.py) to declare VoyageAI's specialized tools. All tools will follow strict ADK conventions (type annotations, robust docstrings, and JSON-serializable outputs).

#### [NEW] [tools.py](file:///Users/alexlopes/.gemini/antigravity/scratch/voyageai/app/tools.py)
* **`search_attractions(location: str, query: str)`**: Simulates an optimized web search to find local attractions, operating hours, ticket costs, and traveler reviews for the target destination.
* **`check_weather(location: str, month: str)`**: Simulates localized weather queries returning seasonal averages (temperature, precipitation, and packing list suggestions).
* **`format_itinerary(itinerary_data: dict)`**: A helper tool that takes a structured daily agenda and renders a formatted markdown guide.

---

### 2. Core Agent, Memory, and Safety Guardrails

 We will modify [agent.py](file:///Users/alexlopes/.gemini/antigravity/scratch/voyageai/app/agent.py) to update our agent prompt, wire up Memory Bank, and enforce prompt hardening.

#### [MODIFY] [agent.py](file:///Users/alexlopes/.gemini/antigravity/scratch/voyageai/app/agent.py)
* **Hardened Prompts**: Update `root_agent` instructions with a strict travel concierge system prompt and Model Armor protections (prompt-injection defense, role preservation).
* **Memory Bank Integration**:
  - Import and register `PreloadMemoryTool` from `google.adk.tools.preload_memory_tool` to fetch long-term user preferences at the start of each turn.
  - Implement a `before_agent_callback` to safely initialize state keys and fallback defaults (e.g. `user_preferences`).
  - Implement an `after_agent_callback` that triggers continuous memory extraction using `await callback_context.add_session_to_memory()`.
* **Robust Project ID Fallback**: Ensure the `GOOGLE_CLOUD_PROJECT` env variable defaults to `"fde-ai-learning-project"` if standard authentication doesn't supply it.

---

### 3. Evaluation Config & Test Cases

We will update our evaluation configs to perform rigorous testing using our custom LLM-as-a-Judge metric.

#### [MODIFY] [eval_config.yaml](file:///Users/alexlopes/.gemini/antigravity/scratch/voyageai/tests/eval/eval_config.yaml)
- Add standard multi-turn metrics: `multi_turn_task_success` and `multi_turn_tool_use_quality`.
- Declare a custom LLM-as-a-Judge metric named `travel_feasibility_judge` to grade physical feasibility, time margins, and user dietary compliance.

#### [MODIFY] [basic-dataset.json](file:///Users/alexlopes/.gemini/antigravity/scratch/voyageai/tests/eval/datasets/basic-dataset.json)
- Add comprehensive test cases to challenge the travel agent (e.g., Tokyo 3-day itinerary request with vegan dietary restrictions and a relaxed pace).

---

## Verification Plan

### Automated Tests
- Run `google-agents-cli eval generate` to simulate conversations across all evaluation cases.
- Run `google-agents-cli eval grade` to execute our custom LLM-as-a-Judge and built-in metrics, showing the results summary.
- Run `uv run pytest` to ensure syntactical and module correctness.

### Manual Verification
- Execute `google-agents-cli playground` to interactively chat with VoyageAI and verify the Memory Bank and tool-calling flows in real-time.
