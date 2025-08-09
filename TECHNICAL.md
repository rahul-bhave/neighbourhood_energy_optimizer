# Technical Architecture — Neighborhood Green Energy Optimizer

## Overview
We use IBM watsonx.ai **Granite models** with the **BeeAI agent framework** in Python to coordinate neighborhood-level renewable energy optimization.

---

## Agents

### 1. Energy Monitor Agent
- Collects generation, load, and storage telemetry (mock APIs for demo).
- Aggregates community energy state.
- Publishes MCP context to other agents.

### 2. Optimization Agent
- Consumes MCP context from Energy Monitor.
- Calls Granite models to generate **human-readable scheduling proposals**.
- Uses deterministic scheduling logic to enforce safe/optimal load shifts.
- Negotiates via ACP messages with Incentives Agent and households.

### 3. Incentives Agent
- Tracks participation, calculates kWh & cost savings.
- Awards points & maintains leaderboard.
- Uses LLM for friendly user-facing messaging.

---

## Agent Communication Protocol (ACP)
A JSON message envelope:
```json
{
  "msg_id": "uuid",
  "from": "agent_name",
  "to": "agent_name",
  "type": "proposal|state_update|confirm|ack",
  "mcp_context_id": "uuid",
  "payload": {},
  "timestamp": 1691838740.123
}
```

---

## Model Context Protocol (MCP)
A structured context object passed into each LLM call:
```json
{
  "neighborhood_state": {
    "total_gen_kw": 5.5,
    "total_load_kw": 3.0,
    "surplus_kw": 2.5
  },
  "user_profiles": {
    "house_1": { "flexible_loads": ["EV", "laundry"] }
  },
  "task_state": {},
  "tool_manifest": {}
}
```

---

## IBM watsonx.ai Granite Usage
Example Python SDK call:
```python
from ibm_watsonx_ai.foundation_models import ModelInference
import os

model = ModelInference(
    model_id="granite-13b-chat-v2",
    project_id=os.environ["WATSONX_PROJECT_ID"],
    api_key=os.environ["WATSONX_APIKEY"],
    url=os.environ["WATSONX_URL"]
)

resp = model.generate(
    prompt="Neighborhood state: {...}. Suggest optimal schedule.",
    max_new_tokens=200
)

print(resp['results'][0]['generated_text'])
```

---

## Safety & Compliance
- Synthetic data only (no PI).
- MCP enforces policy tags to avoid unsafe tool calls.
- All model calls logged for transparency.

---

## Scaling Potential
- Works with any community having basic smart meter APIs.
- Extendable to EV fleets, microgrids, and demand-response programs.
