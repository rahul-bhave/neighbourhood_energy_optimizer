import os
from dotenv import load_dotenv
load_dotenv()
USE_WATSONX = os.getenv('USE_WATSONX','false').lower() == 'true'
if USE_WATSONX:
    try:
        from ibm_watsonx_ai.foundation_models import ModelInference
        watsonx_client = ModelInference(
            model_id=os.getenv('WATSONX_MODEL','granite-13b-chat-v2'),
            project_id=os.getenv('WATSONX_PROJECT_ID'),
            api_key=os.getenv('WATSONX_APIKEY'),
            url=os.getenv('WATSONX_URL')
        )
    except Exception as e:
        print('Failed to init watsonx client:', e)
        watsonx_client = None
else:
    class MockLLM:
        def generate(self, prompt, **kwargs):
            return {'results':[{'generated_text': 'Based on data, encourage more solar adoption.'}]}
    watsonx_client = MockLLM()
def generate_prompt(prompt):
    if USE_WATSONX and watsonx_client:
        return watsonx_client.generate(prompt, max_new_tokens=120)
    else:
        return watsonx_client.generate(prompt)
