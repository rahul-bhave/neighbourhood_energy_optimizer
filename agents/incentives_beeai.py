from beeai.agent import Agent, run_agent
from beeai.serve.acp import Client as AcpClient
from llm.watson_client import generate_prompt, prompt_templates
import time

class IncentivesAgent(Agent):
    def __init__(self, name, mcp_client, **kwargs):
        super().__init__(name=name, **kwargs)
        self.mcp_client = mcp_client
        self.acp = AcpClient()

    async def start(self):
        await super().start()
        self.create_task(self.loop_incentives())

    async def loop_incentives(self):
        while True:
            try:
                msg = self.acp.recv(timeout=1.0)
                if not msg:
                    await self.sleep(0.1)
                    continue
                if msg.get('type') == 'state_update':
                    resp = self.mcp_client.request({'cmd':'get_consumer_summary'})
                    if not resp.get('ok'):
                        self.log('[Incentives] MCP error: %s' % resp)
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
                            discount = 0.10
                        results.append({'consumer_id': c['consumer_id'], 'avg_kwh': c['avg_kwh'], 'discount': discount})
                    for r in results[:10]:
                        prompt = prompt_templates['incentive_notification'].format(consumer_id=r['consumer_id'], avg_kwh=r['avg_kwh'], discount=int(r['discount']*100))
                        resp_text = generate_prompt(prompt)
                        text = resp_text.get('results',[{}])[0].get('generated_text') if isinstance(resp_text, dict) else str(resp_text)
                        self.log(f"NOTIFICATION for {r['consumer_id']}: {text}")
                    if not results:
                        self.log('No consumers met eligibility criteria.')
            except Exception as e:
                self.log('[Incentives] exception: %s' % str(e))
            await self.sleep(0.1)

def run_incentives(mcp_client):
    agent = IncentivesAgent(name='incentives', mcp_client=mcp_client)
    run_agent(agent)
