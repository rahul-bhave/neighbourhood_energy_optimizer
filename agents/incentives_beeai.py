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

    def determine_discount_scenario(self, consumer_data):
        """Determine the discount scenario based on consumer data"""
        avg_kwh = consumer_data['avg_kwh']
        uses_efficient = consumer_data['uses_efficient_equipment']
        produces_solar = consumer_data['produces_solar']
        
        if avg_kwh < 4.0:
            if uses_efficient and produces_solar:
                return '10_percent'
            elif uses_efficient:
                return '5_percent_efficient'
            elif produces_solar:
                return '5_percent_solar'
            else:
                return 'no_discount_low_usage'
        else:
            return 'high_usage'

    def generate_notification_message(self, consumer, scenario):
        """Generate a personalized notification message using LLM"""
        consumer_id = consumer['consumer_id']
        avg_kwh = consumer['avg_kwh']
        uses_efficient = consumer['uses_efficient_equipment']
        produces_solar = consumer['produces_solar']
        
        # Create a detailed prompt for the LLM
        if scenario == '10_percent':
            prompt = f"""Write a complete energy efficiency notification letter for consumer {consumer_id}.

Consumer Details:
- Average daily usage: {avg_kwh} kWh/day
- Uses energy efficient equipment: {uses_efficient}
- Produces solar energy: {produces_solar}
- Usage is below 4 kWh threshold: Yes
- Eligible for 10% discount: Yes

Write a complete congratulatory letter that includes:
1. Greeting with consumer ID
2. Mention their specific usage ({avg_kwh} kWh/day) and that it's below 4 kWh threshold
3. Explain they qualify for 10% discount due to low usage + efficient equipment + solar
4. Thank them for helping reduce carbon emissions
5. Sign off as "Your Community Energy Team"

Write the complete letter:"""
        
        elif scenario == '5_percent_efficient':
            prompt = f"""Write a complete energy efficiency notification letter for consumer {consumer_id}.

Consumer Details:
- Average daily usage: {avg_kwh} kWh/day
- Uses energy efficient equipment: {uses_efficient}
- Produces solar energy: {produces_solar}
- Usage is below 4 kWh threshold: Yes
- Eligible for 5% discount: Yes (efficient equipment)

Write a complete letter that includes:
1. Greeting with consumer ID
2. Mention their specific usage ({avg_kwh} kWh/day) and that it's below 4 kWh threshold
3. Explain they qualify for 5% discount due to low usage + efficient equipment
4. Suggest installing solar panels for additional 5% discount
5. Sign off as "Your Community Energy Team"

Write the complete letter:"""
        
        elif scenario == '5_percent_solar':
            prompt = f"""Write a complete energy efficiency notification letter for consumer {consumer_id}.

Consumer Details:
- Average daily usage: {avg_kwh} kWh/day
- Uses energy efficient equipment: {uses_efficient}
- Produces solar energy: {produces_solar}
- Usage is below 4 kWh threshold: Yes
- Eligible for 5% discount: Yes (solar production)

Write a complete letter that includes:
1. Greeting with consumer ID
2. Mention their specific usage ({avg_kwh} kWh/day) and that it's below 4 kWh threshold
3. Explain they qualify for 5% discount due to low usage + solar production
4. Suggest upgrading to energy efficient equipment for additional 5% discount
5. Sign off as "Your Community Energy Team"

Write the complete letter:"""
        
        elif scenario == 'no_discount_low_usage':
            prompt = f"""Write a complete energy efficiency notification letter for consumer {consumer_id}.

Consumer Details:
- Average daily usage: {avg_kwh} kWh/day
- Uses energy efficient equipment: {uses_efficient}
- Produces solar energy: {produces_solar}
- Usage is below 4 kWh threshold: Yes
- Eligible for discount: No (missing efficient equipment and solar)

Write a complete letter that includes:
1. Greeting with consumer ID
2. Congratulate them on low usage ({avg_kwh} kWh/day) and being below 4 kWh threshold
3. Explain they're not eligible for discounts yet
4. List what they need to do to qualify:
   - Install energy efficient equipment (5% discount)
   - Add solar panels (5% discount)
   - Or both for 10% discount
5. Sign off as "Your Community Energy Team"

Write the complete letter:"""
        
        elif scenario == 'high_usage':
            prompt = f"""Write a complete energy efficiency notification letter for consumer {consumer_id}.

Consumer Details:
- Average daily usage: {avg_kwh} kWh/day
- Uses energy efficient equipment: {uses_efficient}
- Produces solar energy: {produces_solar}
- Usage is above 4 kWh threshold: Yes
- Eligible for discount: No (high usage)

Write a complete letter that includes:
1. Greeting with consumer ID
2. Mention their current usage ({avg_kwh} kWh/day)
3. Explain they need to reduce usage to below 4 kWh/day to qualify
4. List all steps to qualify for discounts:
   - Reduce usage to below 4 kWh/day
   - Install energy efficient equipment (5% discount)
   - Add solar panels (5% discount)
   - Or all three for 10% discount
5. Sign off as "Your Community Energy Team"

Write the complete letter:"""
        
        else:
            prompt = f"""Write a complete energy efficiency notification letter for consumer {consumer_id}.

Consumer Details:
- Average daily usage: {avg_kwh} kWh/day
- Uses energy efficient equipment: {uses_efficient}
- Produces solar energy: {produces_solar}

Write a complete helpful letter with personalized energy efficiency recommendations.
Sign off as "Your Community Energy Team"

Write the complete letter:"""
        
        # Use LLM to generate the message
        try:
            resp_text = generate_prompt(prompt)
            if isinstance(resp_text, dict) and 'results' in resp_text:
                text = resp_text['results'][0].get('generated_text', '')
                # Clean up the response
                if '[MOCK LLM]' in text:
                    # Remove the mock prefix and use the rest
                    text = text.replace('[MOCK LLM]\n', '').replace('[MOCK LLM]', '')
                
                # If the response is too short or incomplete, use fallback
                if len(text.strip()) < 100 or 'Dear' not in text:
                    return self._get_fallback_message(consumer, scenario)
                
                return text.strip()
            else:
                return self._get_fallback_message(consumer, scenario)
        except Exception as e:
            print(f"[Incentives] LLM generation failed: {e}")
            return self._get_fallback_message(consumer, scenario)

    def _get_fallback_message(self, consumer, scenario):
        """Fallback to template messages if LLM fails"""
        consumer_id = consumer['consumer_id']
        avg_kwh = consumer['avg_kwh']
        
        if scenario == '10_percent':
            return f"""Dear {consumer_id},

Congratulations! Your average energy usage over the past month was {avg_kwh} kWh/day, which is below the 4 kWh threshold.

You are using Energy Efficient equipment and have produced solar energy. You are eligible for a 10% discount on your next bill!

This is the highest discount tier available, recognizing your outstanding commitment to energy efficiency and renewable energy production. Your efforts are helping our community reduce carbon emissions and move toward a more sustainable future.

Thank you for being a leader in energy conservation!

-- Your Community Energy Team"""
        
        elif scenario == '5_percent_efficient':
            return f"""Dear {consumer_id},

Great news! Your average energy usage over the past month was {avg_kwh} kWh/day, which is below the 4 kWh threshold.

You are using Energy Efficient equipment. You are eligible for a 5% discount on your next bill!

To qualify for an additional 5% discount (total 10%), consider installing solar panels. This would not only increase your savings but also contribute to our community's renewable energy goals.

Keep up the great work with energy efficiency!

-- Your Community Energy Team"""
        
        elif scenario == '5_percent_solar':
            return f"""Dear {consumer_id},

Excellent! Your average energy usage over the past month was {avg_kwh} kWh/day, which is below the 4 kWh threshold.

You have produced solar energy. You are eligible for a 5% discount on your next bill!

To qualify for an additional 5% discount (total 10%), consider upgrading to Energy Efficient equipment. This combination of solar production and efficient appliances would maximize your savings and environmental impact.

Your solar contribution is making a difference!

-- Your Community Energy Team"""
        
        elif scenario == 'no_discount_low_usage':
            return f"""Dear {consumer_id},

Your average energy usage over the past month was {avg_kwh} kWh/day, which is below the 4 kWh threshold - great job on keeping your consumption low!

However, you are not currently eligible for discounts. To qualify for discounts:

• Install Energy Efficient equipment (5% discount)
• Add solar panels (5% discount)
• Or both for a 10% discount!

You're already on the right track with low usage. These additional steps would help you save money while contributing to our community's sustainability goals.

We're here to help you make these improvements!

-- Your Community Energy Team"""
        
        elif scenario == 'high_usage':
            return f"""Dear {consumer_id},

Your average energy usage over the past month was {avg_kwh} kWh/day.

To qualify for discounts and reduce your energy costs:

• Reduce usage to below 4 kWh/day
• Install Energy Efficient equipment (5% discount)
• Add solar panels (5% discount)
• Or all three for a 10% discount!

We understand that reducing energy usage can be challenging. Our team can provide personalized recommendations to help you achieve these goals. Small changes like using energy-efficient appliances, adjusting thermostat settings, and shifting high-usage activities to off-peak hours can make a significant difference.

Let's work together to reduce your energy costs and environmental impact!

-- Your Community Energy Team"""
        
        else:
            return f"""Dear {consumer_id},

Your average energy usage over the past month was {avg_kwh} kWh/day.

We're here to help you optimize your energy consumption and potentially qualify for discounts. Our team can provide personalized energy efficiency recommendations based on your specific situation.

Please contact us for a detailed energy audit and customized recommendations to help you save money and reduce your environmental impact.

-- Your Community Energy Team"""

    async def loop_incentives(self, completion_event=None):
        processed_once = False
        while True:
            try:
                # Listen for state updates from monitor agent
                emitter = self._create_emitter()
                # For now, simulate receiving a message every few seconds
                # In a real implementation, you would use emitter.on() to listen for events
                await asyncio.sleep(2)  # Wait for potential messages
                
                # Simulate a state update message for testing
                msg = {'type': 'state_update', 'payload': {'summary_count': 50}}
                
                if msg.get('type') == 'state_update' and not processed_once:
                    resp = await asyncio.to_thread(self.mcp_client.request, {'cmd':'get_consumer_summary'})
                    if not resp.get('ok'):
                        print(f'[Incentives] MCP error: {resp}')
                        continue
                    
                    data = resp.get('data', [])
                    print(f'[Incentives] Processing {len(data)} consumers...')
                    
                    # Process all consumers and categorize them
                    scenarios = {
                        '10_percent': [],
                        '5_percent_efficient': [],
                        '5_percent_solar': [],
                        'no_discount_low_usage': [],
                        'high_usage': []
                    }
                    
                    for consumer in data:
                        scenario = self.determine_discount_scenario(consumer)
                        scenarios[scenario].append(consumer)
                    
                    # Print summary
                    print(f'[Incentives] Summary:')
                    print(f'  - 10% discount eligible: {len(scenarios["10_percent"])}')
                    print(f'  - 5% discount (efficient): {len(scenarios["5_percent_efficient"])}')
                    print(f'  - 5% discount (solar): {len(scenarios["5_percent_solar"])}')
                    print(f'  - No discount (low usage): {len(scenarios["no_discount_low_usage"])}')
                    print(f'  - High usage: {len(scenarios["high_usage"])}')
                    
                    # Generate notifications for each scenario
                    for scenario, consumers in scenarios.items():
                        if consumers:
                            print(f'\n[Incentives] Processing {scenario} scenario ({len(consumers)} consumers):')
                            for consumer in consumers:  # Show ALL consumers in each category
                                message = self.generate_notification_message(consumer, scenario)
                                print(f"NOTIFICATION for {consumer['consumer_id']}:")
                                print(message)
                                print("-" * 80)
                    
                    if not any(scenarios.values()):
                        print('No consumers found in data.')
                    
                    # Mark as processed and signal completion
                    processed_once = True
                    print(f'[Incentives] Completed processing all {len(data)} consumers.')
                    if completion_event:
                        completion_event.set()
                    break
                        
            except Exception as e:
                print(f'[Incentives] exception: {str(e)}')
            await asyncio.sleep(0.1)

def run_incentives(mcp_client, shared_emitter=None, completion_event=None):
    agent = IncentivesAgent(name='incentives', mcp_client=mcp_client)
    if shared_emitter:
        agent._emitter = shared_emitter
    
    # Create a wrapper to pass completion_event to the async method
    async def run_with_completion():
        await agent.loop_incentives(completion_event)
    
    # Run the agent using the run method
    import asyncio
    asyncio.run(run_with_completion())
