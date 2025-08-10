import os, time, threading
from dotenv import load_dotenv
load_dotenv()

# regenerate mock DB so every run has fresh data
import logging
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logging.info("Regenerating mock DB...")
import scripts.generate_mock_db as gen_db
gen_db.create_db()
logging.info("Mock DB regenerated.")

# start MCP client (spawns mcp_server as subprocess)
from mcp.mcp_client import MCPClient
mcp = MCPClient(server_py=os.path.join(os.path.dirname(__file__), '../mcp/mcp_server.py'))

# Try to use BeeAI agent implementations
try:
    from agents.energy_monitor_beeai import run_monitor
    from agents.incentives_beeai import run_incentives
    print("Starting BeeAI agents (monitor + incentives)...")
    # run both agents in separate threads since run_agent may block
    t1 = threading.Thread(target=run_monitor, args=(mcp, None), daemon=True)
    t2 = threading.Thread(target=run_incentives, args=(mcp,), daemon=True)
    t1.start()
    t2.start()
    # keep main alive
    while True:
        time.sleep(0.5)
except Exception as e:
    print("BeeAI runtime or agents failed to start:", e)
    print("Ensure 'beeai-framework' is installed and available.")
    mcp.close()
