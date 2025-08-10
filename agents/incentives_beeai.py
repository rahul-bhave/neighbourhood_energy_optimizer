from beeai_framework.agents.base import BaseAgent
from beeai_framework.emitter.emitter import Emitter
from beeai_framework.memory import UnconstrainedMemory
from llm.watson_client import generate_prompt, prompt_templates
import time
import asyncio

class IncentivesAgent(BaseAgent):
    def __init__(self, name, mcp_client, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.mcp_client = mcp_client
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
        await self.loop_incentives()

    async def loop_incentives(self):
        while True:
            try:
                # Listen for state updates from monitor agent
                emitter = self._create_emitter()
                # For now, simulate receiving a message every few seconds
                # In a real implementation, you would use emitter.on() to listen for events
                await asyncio.sleep(2)  # Wait for potential messages
                
                # Simulate a state update message for testing
                msg = {'type': 'state_update', 'payload': {'summary_count': 5}}
                
                if msg.get('type') == 'state_update':
                    resp = await asyncio.to_thread(self.mcp_client.request, {'cmd':'get_consumer_summary'})
                    if not resp.get('ok'):
                        print(f'[Incentives] MCP error: {resp}')
                        continue
                    data = resp.get('data', [])
                    eligible = [d for d in data if d['avg_kwh'] < 5.0 and d['uses_efficient_equipment'] and d['produces_solar']]
                    eligible_sorted = sorted(eligible, key=lambda x: x['avg_kwh'])
                    results = []
                    for idx, c in enumerate(eligible_sorted):
                        if idx == 0:
                            discount = 0.15
                        elif idx == 1:
                            discount = 0.10
                        else:
                            discount = 0.05
                        results.append({'consumer_id': c['consumer_id'], 'avg_kwh': c['avg_kwh'], 'discount': discount})
                    for r in results[:10]:
                        prompt = prompt_templates['incentive_notification'].format(consumer_id=r['consumer_id'], avg_kwh=r['avg_kwh'], discount=int(r['discount']*100))
                        resp_text = generate_prompt(prompt)
                        text = resp_text.get('results',[{}])[0].get('generated_text') if isinstance(resp_text, dict) else str(resp_text)
                        print(f"NOTIFICATION for {r['consumer_id']}: {text}")
                    if not results:
                        print('No consumers met eligibility criteria.')
            except Exception as e:
                print(f'[Incentives] exception: {str(e)}')
            await asyncio.sleep(0.1)

def run_incentives(mcp_client, shared_emitter=None):
    agent = IncentivesAgent(name='incentives', mcp_client=mcp_client)
    if shared_emitter:
        agent._emitter = shared_emitter
    # Run the agent using the run method
    import asyncio
    asyncio.run(agent.run())
