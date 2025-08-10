import os
import logging
from dotenv import load_dotenv
load_dotenv()
USE_WATSONX = os.getenv('USE_WATSONX','false').lower() == 'true'
MODEL = os.getenv('WATSONX_MODEL','ibm/granite-3-2-8b-instruct')

# Debug logging
logging.info(f"USE_WATSONX: {USE_WATSONX}")
logging.info(f"WATSONX_MODEL: {MODEL}")

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
        # Check if credentials are available
        api_key = os.getenv('WATSONX_API_KEY') or os.getenv('WATSONX_APIKEY')
        project_id = os.getenv('WATSONX_PROJECT_ID')
        
        # Debug logging
        logging.info(f"API Key found: {bool(api_key)}")
        logging.info(f"Project ID found: {bool(project_id)}")
        
        if not api_key:
            logging.warning("WATSONX_API_KEY environment variable is not set, using mock client")
            client = None
        elif not project_id:
            logging.warning("WATSONX_PROJECT_ID environment variable is not set, using mock client")
            client = None
        else:
            logging.info("Initializing Watsonx ModelInference client...")
            # Initialize with credentials dict
            try:
                credentials = {
                    "apikey": api_key,
                    "url": os.getenv('WATSONX_URL', 'https://us-south.ml.cloud.ibm.com')
                }
                client = ModelInference(
                    model_id=MODEL,
                    project_id=project_id,
                    credentials=credentials
                )
                logging.info("Watsonx client initialized successfully with credentials dict")
            except Exception as e:
                logging.warning(f"Watsonx initialization failed: {e}")
                client = None
    except Exception as e:
        logging.warning('Watsonx init failed: %s', e)
        client = None
else:
    class MockLLM:
        def generate(self, prompt, **kwargs):
            return {'results':[{'generated_text': '[MOCK LLM]\n' + prompt}]}
    client = MockLLM()

def generate_prompt(prompt):
    if USE_WATSONX and client:
        try:
            # Use the correct parameters for IBM Watsonx AI
            resp = client.generate(prompt=prompt)
            return resp
        except Exception as e:
            logging.warning(f'Watsonx generate failed: {e}, using mock response')
            return {'results':[{'generated_text': '[MOCK LLM - Watsonx failed]\n' + prompt}]}
    else:
        # Use mock client when Watsonx is disabled or client is None
        if client is None:
            return {'results':[{'generated_text': '[MOCK LLM - No client]\n' + prompt}]}
        return client.generate(prompt)

