from beeai_framework.agents.base import BaseAgent
from beeai_framework.emitter.emitter import Emitter
from beeai_framework.memory import UnconstrainedMemory
from llm.watson_client import generate_prompt, prompt_templates
import time
import asyncio

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

    def get_scenario_color(self, scenario):
        """Get color for different discount scenarios"""
        colors = {
            '10_percent': Colors.OKGREEN + Colors.BOLD,  # Bright green for highest discount
            '5_percent_efficient': Colors.OKCYAN + Colors.BOLD,  # Cyan for efficient equipment
            '5_percent_solar': Colors.PURPLE + Colors.BOLD,  # Purple for solar
            'no_discount_low_usage': Colors.YELLOW + Colors.BOLD,  # Yellow for no discount
            'high_usage': Colors.WARNING + Colors.BOLD  # Orange for high usage
        }
        return colors.get(scenario, Colors.ENDC)

    def get_scenario_icon(self, scenario):
        """Get icon for different discount scenarios"""
        icons = {
            '10_percent': '[TOP]',
            '5_percent_efficient': '[EFF]',
            '5_percent_solar': '[SOL]',
            'no_discount_low_usage': '[INFO]',
            'high_usage': '[HIGH]'
        }
        return icons.get(scenario, '[GEN]')

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
            print_colored(f"[Incentives] LLM generation failed: {e}", Colors.FAIL)
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
• Or all three for 10% discount!

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
        processed_consumers = 0
        total_consumers = 0
        
        while True:
            try:
                # Listen for individual consumer data from monitor agent
                emitter = self._create_emitter()
                
                # Simulate receiving consumer data (in real implementation, you'd listen for events)
                if processed_consumers == 0:
                    # Get all consumers to know the total count
                    resp = await asyncio.to_thread(self.mcp_client.request, {'cmd':'get_consumer_summary'})
                    if not resp.get('ok'):
                        print_colored(f'[Incentives] MCP error: {resp}', Colors.FAIL)
                        continue
                    
                    all_consumers = resp.get('data', [])
                    total_consumers = len(all_consumers)
                    print_colored(f'[Incentives] *** Ready to process {total_consumers} consumers one by one... ***', Colors.OKCYAN + Colors.BOLD)
                
                # Process one consumer at a time
                if processed_consumers < total_consumers:
                    consumer = all_consumers[processed_consumers]
                    
                    # Determine scenario for this consumer
                    scenario = self.determine_discount_scenario(consumer)
                    scenario_color = self.get_scenario_color(scenario)
                    scenario_icon = self.get_scenario_icon(scenario)
                    
                    # Generate and display notification
                    print_colored(f'\n[Incentives] {scenario_icon} Processing consumer {processed_consumers + 1}/{total_consumers}: {consumer["consumer_id"]} ({scenario})', scenario_color)
                    message = self.generate_notification_message(consumer, scenario)
                    
                    # Print notification with scenario-specific color
                    print_colored(f"NOTIFICATION for {consumer['consumer_id']}:", scenario_color)
                    print_colored(message, Colors.ENDC)
                    print_colored("-" * 80, Colors.OKBLUE)
                    
                    # Send acknowledgment back to monitor
                    ack_msg = {
                        'msg_id': f'incentives-ack-{processed_consumers}',
                        'from': 'incentives',
                        'to': 'monitor',
                        'type': 'consumer_processed',
                        'payload': {
                            'consumer_id': consumer['consumer_id'],
                            'scenario': scenario,
                            'processed_index': processed_consumers
                        }
                    }
                    await emitter.emit('consumer_processed', ack_msg)
                    print_colored(f"[Incentives] > Acknowledged processing of {consumer['consumer_id']}", Colors.OKGREEN)
                    
                    processed_consumers += 1
                    
                    # Small delay to simulate processing time
                    await asyncio.sleep(0.5)
                    
                else:
                    # All consumers processed
                    print_colored(f'\n[Incentives] *** Completed processing all {total_consumers} consumers. ***', Colors.OKGREEN + Colors.BOLD)
                    print_colored(f'[Incentives] *** Summary of processed consumers: ***', Colors.HEADER + Colors.BOLD)
                    
                    # Generate summary
                    scenarios = {
                        '10_percent': 0,
                        '5_percent_efficient': 0,
                        '5_percent_solar': 0,
                        'no_discount_low_usage': 0,
                        'high_usage': 0
                    }
                    
                    for consumer in all_consumers:
                        scenario = self.determine_discount_scenario(consumer)
                        scenarios[scenario] += 1
                    
                    # Print summary with colors
                    print_colored(f'  [TOP] 10% discount eligible: {scenarios["10_percent"]}', Colors.OKGREEN + Colors.BOLD)
                    print_colored(f'  [EFF] 5% discount (efficient): {scenarios["5_percent_efficient"]}', Colors.OKCYAN + Colors.BOLD)
                    print_colored(f'  [SOL] 5% discount (solar): {scenarios["5_percent_solar"]}', Colors.PURPLE + Colors.BOLD)
                    print_colored(f'  [INFO] No discount (low usage): {scenarios["no_discount_low_usage"]}', Colors.YELLOW + Colors.BOLD)
                    print_colored(f'  [HIGH] High usage: {scenarios["high_usage"]}', Colors.WARNING + Colors.BOLD)
                    
                    if completion_event:
                        completion_event.set()
                    break
                        
            except Exception as e:
                print_colored(f'[Incentives] *** Exception: {str(e)} ***', Colors.FAIL)
                await asyncio.sleep(1)

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
