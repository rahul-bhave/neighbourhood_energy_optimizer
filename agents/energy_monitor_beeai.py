from beeai_framework.agents.base import BaseAgent
from beeai_framework.emitter.emitter import Emitter
from beeai_framework.memory import UnconstrainedMemory
from mcp.store import create_mcp
import time
import asyncio

class EnergyMonitorAgent(BaseAgent):
    def __init__(self, name, mcp_client, db_path, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.mcp_client = mcp_client
        self.db_path = db_path
        self._emitter = None

    @property
    def memory(self):
        # Return a simple memory implementation
        from beeai_framework.memory import UnconstrainedMemory
        return UnconstrainedMemory()

    def _create_emitter(self):
        # Create a simple emitter for inter-agent communication
        if self._emitter is None:
            self._emitter = Emitter()
        return self._emitter

    async def run(self):
        # Main run method
        # Initialize the agent
        # Run the main loop directly
        await self.loop_monitor()

    async def loop_monitor(self, completion_event=None):
        processed_count = 0
        while True:
            try:
                resp = await asyncio.to_thread(self.mcp_client.request, {'cmd':'get_consumer_summary'})
                if not resp.get('ok'):
                    print(f'[Monitor] MCP error: {resp}')
                    await asyncio.sleep(2)
                    continue
                data = resp.get('data', [])
                total_load = sum(d['avg_kwh'] for d in data)
                total_gen = max(0, len(data) * 1.5 - total_load/10)
                state = {'total_gen_kw': total_gen, 'total_load_kw': total_load, 'surplus_kw': max(0, total_gen - total_load)}
                profiles = {d['consumer_id']:{'uses_efficient_equipment':d['uses_efficient_equipment'], 'produces_solar':d['produces_solar']} for d in data}
                mcp_id = create_mcp(state, profiles, {}, {})
                # send state_update via emitter
                msg = {'msg_id': self.name + '-state', 'from': self.name, 'to': 'incentives', 'type': 'state_update', 'mcp_context_id': mcp_id, 'payload': {'summary_count': len(data)}}
                emitter = self._create_emitter()
                await emitter.emit('state_update', msg)
                print(f"[Monitor] Sent state update: {msg}")
                
                # Track processing and signal completion
                processed_count += 1
                if processed_count >= 5:  # Process 5 cycles then signal completion
                    print(f"[Monitor] Completed processing cycles. Signaling completion...")
                    if completion_event:
                        completion_event.set()
                    break
                    
            except Exception as e:
                print(f'[Monitor] exception: {str(e)}')
            await asyncio.sleep(2)

def run_monitor(mcp_client, db_path, shared_emitter=None, completion_event=None):
    agent = EnergyMonitorAgent(name='monitor', mcp_client=mcp_client, db_path=db_path)
    if shared_emitter:
        agent._emitter = shared_emitter
    
    # Create a wrapper to pass completion_event to the async method
    async def run_with_completion():
        await agent.loop_monitor(completion_event)
    
    # Run the agent using the run method
    import asyncio
    asyncio.run(run_with_completion())
