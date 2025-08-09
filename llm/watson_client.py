import os
from dotenv import load_dotenv
load_dotenv()
USE_WATSONX = os.getenv('USE_WATSONX','false').lower() == 'true'
MODEL = os.getenv('WATSONX_MODEL','granite-13b-chat-v2')

prompt_templates = {
    'incentive_notification': """Dear {consumer_id},
Congratulations! Your average energy usage over the past month was {avg_kwh} kWh/day.
As a reward for using energy-efficient equipment and producing solar power, you have been awarded a {discount}% discount on your next bill.
Thank you for helping the community reduce carbon emissions.
-- Your Community Energy Team""",

    'recommendation': """Dear {consumer_id},
Your average energy usage is {avg_kwh} kWh/day. Based on our analysis, we recommend: {recs}.
Small changes like adopting energy-efficient appliances or shifting EV charging to daytime can reduce your bill.
-- Your Community Energy Team"""
}

if USE_WATSONX:
    try:
        from ibm_watsonx_ai.foundation_models import ModelInference
        client = ModelInference(
            model_id=MODEL,
            project_id=os.getenv('WATSONX_PROJECT_ID'),
            api_key=os.getenv('WATSONX_APIKEY'),
            url=os.getenv('WATSONX_URL')
        )
    except Exception as e:
        print('Watsonx init failed:', e)
        client = None
else:
    class MockLLM:
        def generate(self, prompt, **kwargs):
            return {'results':[{'generated_text': '[MOCK LLM]\\n' + prompt}]}
    client = MockLLM()

def generate_prompt(prompt):
    if USE_WATSONX and client:
        resp = client.generate(prompt=prompt, max_new_tokens=150)
        return resp
    else:
        return client.generate(prompt)

