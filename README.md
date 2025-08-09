# Neighborhood Green Energy Optimizer

**Hackathon:** IBM Watsonx Build with Agentic AI Challenge  
**Theme:** Everyday community problem solved with multi-agent AI  
**Team:** [Your Team Name]  

---

## Problem
Neighborhoods with solar/battery resources often waste surplus clean energy when demand is low, then pull from fossil-fuel grid during peaks.  
Lack of coordination reduces renewable utilization, raises bills, and strains the grid.

---

## Solution
We built a **multi-agent system** using IBM watsonx.ai Granite models + BeeAI framework to coordinate flexible household loads (e.g., EV charging, laundry, water heating) to match renewable generation.  
Agents communicate via an **Agent Communication Protocol (ACP)** and share consistent context using a **Model Context Protocol (MCP)**.

### Agents
1. **Energy Monitor Agent** — aggregates live telemetry from households.
2. **Optimization Agent** — proposes optimal load schedules based on real-time + forecast data.
3. **Incentives Agent** — gamifies participation with points & leaderboards.

---

## Tech Stack
- **IBM watsonx.ai** — Granite models for reasoning & explanation
- **BeeAI framework** — Python multi-agent orchestration
- **ACP** — JSON-based message envelopes
- **MCP** — structured context for LLM calls
- **Mock APIs** — simulate smart meters, weather feeds

---

## Run the Demo
```bash
pip install -r requirements.txt

export WATSONX_APIKEY="your_api_key"
export WATSONX_PROJECT_ID="your_project_id"
export WATSONX_URL="https://us-south.ml.cloud.ibm.com"

python family_energy_poc.py
```

**Tip:** For the hackathon demo, you can run in `MOCK_MODE=True` to avoid consuming RUs.

---

## Hackathon Deliverables
- [TECHNICAL.md](./TECHNICAL.md) — detailed agentic AI + IBM watsonx usage
- [demo_script.md](./demo_script.md) — 3-minute video storyboard & narration
- `family_energy_poc.py` — runnable proof-of-concept with mock data

---

## License
MIT
