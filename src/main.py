import os, time
from dotenv import load_dotenv
from acp.bus import MessageBus
from mcp.mcp_client import MCPClient
from agents.energy_monitor import EnergyMonitorAgent
from agents.incentives import IncentivesAgent

load_dotenv()

def main():
    bus = MessageBus()
    mcp = MCPClient(server_py=os.path.join(os.path.dirname(__file__), '../mcp/mcp_server.py'))
    db_path = os.path.join(os.path.dirname(__file__), '../data/mock_data.db')
    monitor = EnergyMonitorAgent('monitor', bus, mcp, db_path)
    incentives = IncentivesAgent('incentives', bus, mcp)
    monitor.start()
    incentives.start()
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print('shutting down...')
        mcp.close()

if __name__ == '__main__':
    main()
