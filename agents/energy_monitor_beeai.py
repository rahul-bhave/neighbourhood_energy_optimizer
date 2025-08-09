from beeai.agent import Agent, run_agent
from beeai.serve.acp import Client as AcpClient
from mcp.store import create_mcp
import time

class EnergyMonitorAgent(Agent):
    def __init__(self, name, mcp_client, db_path, **kwargs):
        super().__init__(name=name, **kwargs)
        self.mcp_client = mcp_client
        self.db_path = db_path
        self.acp = AcpClient()

    async def start(self):
        await super().start()
        # schedule the main loop as an async background task
        self.create_task(self.loop_monitor())

    async def loop_monitor(self):
        while True:
            try:
                resp = self.mcp_client.request({'cmd':'get_consumer_summary'})
                if not resp.get('ok'):
                    self.log('[Monitor] MCP error: %s' % resp)
                    await self.sleep(2)
                    continue
                data = resp.get('data', [])
                total_load = sum(d['avg_kwh'] for d in data)
                total_gen = max(0, len(data) * 1.5 - total_load/10)
                state = {'total_gen_kw': total_gen, 'total_load_kw': total_load, 'surplus_kw': max(0, total_gen - total_load)}
                profiles = {d['consumer_id']:{'uses_efficient_equipment':d['uses_efficient_equipment'], 'produces_solar':d['produces_solar']} for d in data}
                mcp_id = create_mcp(state, profiles, {}, {})
                # send state_update via ACP
                msg = {'msg_id': self.name + '-state', 'from': self.name, 'to': 'incentives', 'type': 'state_update', 'mcp_context_id': mcp_id, 'payload': {'summary_count': len(data)}}
                self.acp.send(msg)
            except Exception as e:
                self.log('[Monitor] exception: %s' % str(e))
            await self.sleep(2)

def run_monitor(mcp_client, db_path):
    agent = EnergyMonitorAgent(name='monitor', mcp_client=mcp_client, db_path=db_path)
    run_agent(agent)
