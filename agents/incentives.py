import time
from agents.base import BaseAgent
from mcp.store import get_mcp
from acp.envelope import envelope

class IncentivesAgent(BaseAgent):
    def __init__(self, name, bus, mcp_client):
        super().__init__(name, bus)
        self.mcp_client = mcp_client

    def run(self):
        while True:
            msg = self.recv()
            if not msg:
                time.sleep(0.1)
                continue
            if msg.get('type') == 'state_update':
                # fetch summary from MCP server
                resp = self.mcp_client.request({'cmd':'get_consumer_summary'})
                if not resp.get('ok'):
                    print('[Incentives] MCP error', resp)
                    continue
                data = resp.get('data', [])
                # Eligibility: avg_kwh < 5 AND efficient AND solar => eligible
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
                print('--- Incentive Results ---')
                if results:
                    for r in results:
                        print(f"Consumer {r['consumer_id']} => discount {int(r['discount']*100)}% (avg {r['avg_kwh']} kWh)")
                else:
                    print('No consumers met eligibility criteria.')
                # Recommendations for some non-eligible consumers
                noneligible = [d for d in data if d not in eligible_sorted]
                print('--- Recommendations (sample) ---')
                for d in noneligible[:5]:
                    recs = []
                    if not d['uses_efficient_equipment']:
                        recs.append('adopt energy-efficient appliances')
                    if not d['produces_solar']:
                        recs.append('consider rooftop/community solar')
                    if d['avg_kwh'] > 8.0:
                        recs.append('participate in load-shifting programs')
                    print(f"{d['consumer_id']}: {', '.join(recs)}")
