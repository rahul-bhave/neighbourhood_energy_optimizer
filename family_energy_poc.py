import time, uuid, threading, os, sqlite3
from queue import Queue, Empty
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MOCK_MODE = True  # Toggle for live calls

if not MOCK_MODE:
    from ibm_watsonx_ai.foundation_models import ModelInference
    watsonx_client = ModelInference(
        model_id="granite-13b-chat-v2",
        project_id=os.getenv("WATSONX_PROJECT_ID"),
        api_key=os.getenv("WATSONX_APIKEY"),
        url=os.getenv("WATSONX_URL")
    )
else:
    class MockWatsonXClient:
        def generate(self, prompt, **kwargs):
            return {"results":[{"generated_text": "Suggested: EV charge 16:00-18:00 using surplus solar."}]}
    watsonx_client = MockWatsonXClient()

# --- ACP Message Bus ---
class MessageBus:
    def __init__(self): self.queues = {}
    def register(self, name): self.queues.setdefault(name, Queue())
    def send(self, env): self.queues[env["to"]].put(env)
    def recv(self, name, timeout=0.1):
        try: return self.queues[name].get(timeout=timeout)
        except Empty: return None

# --- MCP Store ---
MCP_STORE = {}
def create_mcp(state, profiles, task_state, tools):
    mcp_id = str(uuid.uuid4())
    MCP_STORE[mcp_id] = {
        "neighborhood_state": state,
        "user_profiles": profiles,
        "task_state": task_state,
        "tool_manifest": tools
    }
    return mcp_id

# --- ACP Envelope ---
def envelope(sender, to, mtype, payload, mcp_id):
    return {
        "msg_id": str(uuid.uuid4()),
        "from": sender,
        "to": to,
        "type": mtype,
        "mcp_context_id": mcp_id,
        "payload": payload,
        "timestamp": time.time()
    }

# --- Base Agent ---
class BaseAgent(threading.Thread):
    def __init__(self, name, bus):
        super().__init__(daemon=True)
        self.name, self.bus = name, bus
        self.bus.register(name)
    def send(self, env): self.bus.send(env)
    def recv(self, timeout=0.5): return self.bus.recv(self.name, timeout)

# --- Agents ---
class EnergyMonitorAgent(BaseAgent):
    def __init__(self, name, bus, db_path="mock_data.db"):
        super().__init__(name, bus)
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cur = self.conn.cursor()

    def run(self):
        while True:
            self.cur.execute("""
                SELECT house_id, gen_kw, load_kw, soc_pct
                FROM telemetry
                WHERE timestamp = (SELECT MAX(timestamp) FROM telemetry)
            """)
            rows = self.cur.fetchall()
            total_gen = sum(r[1] for r in rows)
            total_load = sum(r[2] for r in rows)
            surplus = total_gen - total_load
            state = {
                "total_gen_kw": total_gen,
                "total_load_kw": total_load,
                "surplus_kw": surplus
            }
            profiles = {r[0]: {"flexible_loads": ["EV", "laundry"]} for r in rows}
            mcp_id = create_mcp(state, profiles, {}, {})
            env = envelope(self.name, "optimization", "state_update", state, mcp_id)
            self.send(env)
            time.sleep(2)

class OptimizationAgent(BaseAgent):
    def run(self):
        while True:
            msg = self.recv()
            if not msg: continue
            if msg["type"] == "state_update":
                mcp = MCP_STORE[msg["mcp_context_id"]]
                prompt = f"Neighborhood state: {mcp['neighborhood_state']}. Suggest optimal schedule."
                if not MOCK_MODE:
                    resp = watsonx_client.generate(prompt, max_new_tokens=100)
                    proposal_text = resp["results"][0]["generated_text"]
                else:
                    proposal_text = watsonx_client.generate(prompt)["results"][0]["generated_text"]
                proposal = {
                    "proposal_text": proposal_text,
                    "tasks": [{"house": "house_1", "task": "EV_charge", "window": "16:00-18:00"}]
                }
                self.send(envelope(self.name, "incentives", "proposal", proposal, msg["mcp_context_id"]))

class IncentivesAgent(BaseAgent):
    def run(self):
        leaderboard = {}
        while True:
            msg = self.recv()
            if not msg: continue
            if msg["type"] == "proposal":
                for t in msg["payload"]["tasks"]:
                    leaderboard[t["house"]] = leaderboard.get(t["house"], 0) + 10
                print("[Leaderboard]", leaderboard)

# --- Main ---
if __name__ == "__main__":
    bus = MessageBus()
    agents = [
        EnergyMonitorAgent("monitor", bus),
        OptimizationAgent("optimization", bus),
        IncentivesAgent("incentives", bus)
    ]
    for a in agents: a.start()
    try:
        while True: time.sleep(0.5)
    except KeyboardInterrupt:
        print("Stopping...")
