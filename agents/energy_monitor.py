import time
from agents.base import BaseAgent
from acp.envelope import envelope
from mcp.store import create_mcp

class EnergyMonitorAgent(BaseAgent):
    def __init__(self, name, bus, mcp_client, db_path):
        super().__init__(name, bus)
        self.mcp_client = mcp_client
        self.db_path = db_path

    def run(self):
        while True:
            try:
                resp = self.mcp_client.request({'cmd':'get_consumer_summary'})
                if not resp.get('ok'):
                    print('[Monitor] MCP error', resp)
                    time.sleep(2)
                    continue
                data = resp.get('data', [])
                total_load = sum(d['avg_kwh'] for d in data)
                state = {'total_gen_kw': max(0, len(data)*1.5 - total_load/10), 'total_load_kw': total_load, 'surplus_kw': max(0, len(data)*1.5 - total_load/10)}
                profiles = {d['consumer_id']:{'uses_efficient_equipment':d['uses_efficient_equipment'], 'produces_solar':d['produces_solar']} for d in data}
                mcp_id = create_mcp(state, profiles, {}, {})
                env = envelope(self.name, 'incentives', 'state_update', {'summary_count': len(data)}, mcp_id)
                self.send(env)
            except Exception as e:
                print('[Monitor] exception', e)
            time.sleep(2)
