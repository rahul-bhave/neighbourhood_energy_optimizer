import os
import time
import threading
import logging
from dotenv import load_dotenv

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.generate_mock_db import create_db
from mcp.mcp_client import MCPClient
from agents.energy_monitor_beeai import run_monitor
from agents.incentives_beeai import run_incentives
from beeai_framework.emitter.emitter import Emitter


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
    load_dotenv()

    # Fresh mock DB for each run
    create_db()

    # start MCP client (spawns mcp_server as subprocess)
    mcp = MCPClient(server_py=os.path.join(os.path.dirname(__file__), '../mcp/mcp_server.py'))

    # Create shared emitter for inter-agent communication
    shared_emitter = Emitter()

    # Add completion tracking
    completion_event = threading.Event()
    
    logging.info("Starting BeeAI agents (monitor + incentives)...")
    logging.info("Agents will process all 50 consumers and then exit...")
    
    t1 = threading.Thread(target=run_monitor, args=(mcp, None, shared_emitter, completion_event), daemon=True)
    t2 = threading.Thread(target=run_incentives, args=(mcp, shared_emitter, completion_event), daemon=True)
    t1.start()
    t2.start()

    try:
        # Wait for completion or timeout after 60 seconds
        completion_event.wait(timeout=60)
        if completion_event.is_set():
            logging.info('All 50 consumers processed successfully. Shutting down...')
        else:
            logging.info('Timeout reached. Shutting down...')
    except KeyboardInterrupt:
        logging.info('Shutting down...')
    finally:
        mcp.close()


if __name__ == '__main__':
    main()
