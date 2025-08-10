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
        self.processed_consumers = 0
        self.total_consumers = 0

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
        # Get all consumers first
        resp = await asyncio.to_thread(self.mcp_client.request, {'cmd':'get_consumer_summary'})
        if not resp.get('ok'):
            print(f'[Monitor] MCP error: {resp}')
            return
        
        all_consumers = resp.get('data', [])
        self.total_consumers = len(all_consumers)
        print(f'[Monitor] Starting to process {self.total_consumers} consumers one by one...')
        
        # Process each consumer individually
        for i, consumer in enumerate(all_consumers):
            try:
                # Send individual consumer data to incentives agent
                msg = {
                    'msg_id': f'{self.name}-consumer-{i}',
                    'from': self.name,
                    'to': 'incentives',
                    'type': 'consumer_data',
                    'payload': {
                        'consumer': consumer,
                        'consumer_index': i,
                        'total_consumers': self.total_consumers
                    }
                }
                
                emitter = self._create_emitter()
                await emitter.emit('consumer_data', msg)
                print(f"[Monitor] Sent consumer {i+1}/{self.total_consumers}: {consumer['consumer_id']}")
                
                # Wait for acknowledgment from incentives agent
                # In a real implementation, you would listen for the acknowledgment
                await asyncio.sleep(1)  # Simulate processing time
                
                self.processed_consumers += 1
                
            except Exception as e:
                print(f'[Monitor] exception processing consumer {i}: {str(e)}')
        
        print(f"[Monitor] Completed processing all {self.total_consumers} consumers. Signaling completion...")
        if completion_event:
            completion_event.set()

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
