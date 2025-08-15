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

# ANSI Color Codes for colorful output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    PURPLE = '\033[35m'
    YELLOW = '\033[33m'

def print_colored(text, color=Colors.ENDC):
    """Print text with color"""
    try:
        print(f"{color}{text}{Colors.ENDC}")
    except UnicodeEncodeError:
        # Fallback for encoding issues
        print(f"{color}{text.encode('ascii', 'ignore').decode('ascii')}{Colors.ENDC}")

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
    load_dotenv()

    print_colored("*** Neighbourhood Energy Optimizer - Starting System ***", Colors.HEADER + Colors.BOLD)
    print_colored("=" * 70, Colors.OKBLUE)

    # Fresh mock DB for each run
    create_db()

    # start MCP client (spawns mcp_server as subprocess)
    print_colored("> Initializing MCP client...", Colors.OKCYAN)
    mcp = MCPClient(server_py=os.path.join(os.path.dirname(__file__), '../mcp/mcp_server.py'))
    print_colored("> MCP client initialized!", Colors.OKGREEN)

    # Create shared emitter for inter-agent communication
    print_colored("> Setting up agent communication...", Colors.OKCYAN)
    shared_emitter = Emitter()
    print_colored("> Agent communication ready!", Colors.OKGREEN)

    # Add completion tracking
    completion_event = threading.Event()
    
    print_colored("\n*** Starting BeeAI agents (monitor + incentives)... ***", Colors.HEADER + Colors.BOLD)
    print_colored("> Agents will process all 50 consumers sequentially...", Colors.WARNING)
    print_colored("=" * 70, Colors.OKBLUE)
    
    t1 = threading.Thread(target=run_monitor, args=(mcp, None, shared_emitter, completion_event), daemon=True)
    t2 = threading.Thread(target=run_incentives, args=(mcp, shared_emitter, completion_event), daemon=True)
    t1.start()
    t2.start()

    try:
        # Wait for completion or timeout after 60 seconds
        completion_event.wait(timeout=60)
        if completion_event.is_set():
            print_colored("\n" + "=" * 70, Colors.OKBLUE)
            print_colored("*** All 50 consumers processed successfully! ***", Colors.OKGREEN + Colors.BOLD)
            print_colored("> System shutdown complete!", Colors.OKGREEN)
        else:
            print_colored("\n" + "=" * 70, Colors.OKBLUE)
            print_colored("*** Timeout reached. Shutting down... ***", Colors.WARNING + Colors.BOLD)
    except KeyboardInterrupt:
        print_colored("\n" + "=" * 70, Colors.OKBLUE)
        print_colored("*** Manual shutdown requested... ***", Colors.FAIL + Colors.BOLD)
    finally:
        mcp.close()
        print_colored("> Goodbye!", Colors.HEADER)


if __name__ == '__main__':
    main()
