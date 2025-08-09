## Neighborhood Green Energy Optimizer 
An agentic AI solution built with the BeeAI framework and IBM Watsonx Granite LLM to help communities coordinate green energy usage, optimize shared loads, and reward sustainable behavior.Modular Neighborhood Energy Optimizer. See src/main.py to run.
###  Demo Features
1. Two BeeAI Agents:

Energy Monitor Agent — Fetches neighborhood energy stats via MCP.

Incentives Agent — Calculates discounts for eco-friendly homes and generates personalized recommendations.

2. Agent Communication Protocol (ACP) for real-time agent-to-agent messaging.

3. Model Context Protocol (MCP) to connect agents to structured external data.

4. Watsonx Granite Integration for generating natural language outputs.



### 🛠 Requirements
Python 3.10+

IBM Watsonx credentials (only if using live Granite calls)

Install dependencies:

```bash
pip install -r requirements.txt

