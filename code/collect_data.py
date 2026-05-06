import csv
import json
import time
import os
from datetime import datetime
import requests
from config import OPENROUTER_API_KEY, GROQ_API_KEY, MODELS_GROQ
from logger import setup_logger
from error_handler import retry_on_error
from tqdm import tqdm

logger = setup_logger()

class DataCollector:
    def __init__(self):
        self.groq_key = GROQ_API_KEY
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"

    def load_prompts(self, csv_path):
        """Load prompts from CSV file"""
        prompts = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                prompts.append(row)
        return prompts

    def query_groq(self, model, prompt_text):
        """Send prompt to Groq API"""
        headers = {
            "Authorization": f"Bearer {self.groq_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt_text}]
        }
        try:
            response = requests.post(
                self.groq_url,
                headers=headers,
                json=data,
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            return {
                "success": True,
                "response": result['choices'][0]['message']['content'],
                "model": model,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": model,
                "timestamp": datetime.now().isoformat()
            }

    def save_response(self, prompt_data, model, response_data):
        """Save model response to JSON file"""
        model_name = model.split('/')[-1].replace(':', '-')
        output_dir = f"data/responses/{model_name}"
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"{output_dir}/prompt_{prompt_data['id']}.json"
        data = {
            "prompt_id": prompt_data['id'],
            "category": prompt_data['category'],
            "subcategory": prompt_data['subcategory'],
            "prompt": prompt_data['prompt'],
            "expected_response": prompt_data['expected_response'],
            "sensitivity_level": prompt_data['sensitivity_level'],
            "model": model,
            "response": response_data['response'] if response_data['success'] else None,
            "error": response_data.get('error'),
            "timestamp": response_data['timestamp']
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return filename

    def collect_all(self, csv_path, models):
        """Main data collection loop"""
        prompts = self.load_prompts(csv_path)
        total = len(prompts) * len(models)
        current = 0

        logger.info(f"Starting data collection...")
        logger.info(f"Total prompts: {len(prompts)}")
        logger.info(f"Models: {len(models)}")
        logger.info(f"Total requests: {total}")

        for prompt in tqdm(prompts, desc="Processing prompts"):
            logger.info(f"--- Prompt {prompt['id']}/{len(prompts)} ---")
            logger.info(f"Category: {prompt['category']} ({prompt['subcategory']})")
            logger.info(f"Text: {prompt['prompt'][:60]}...")

            for model in models:
                current += 1
                logger.info(f"[{current}/{total}] Testing model: {model}")

                response = retry_on_error(
                    lambda m=model, p=prompt['prompt']: self.query_groq(m, p),
                    max_retries=3,
                    delay=5
                )

                if response is None:
                    response = {
                        "success": False,
                        "error": "Failed after 3 retries",
                        "model": model,
                        "timestamp": datetime.now().isoformat()
                    }

                filename = self.save_response(prompt, model, response)

                if response['success']:
                    logger.info(f"Success - saved to {filename}")
                    logger.info(f"Response preview: {response['response'][:100]}...")
                else:
                    logger.error(f"Error: {response['error']}")

                # Pause between requests
                time.sleep(2)

        logger.info(f"Collection complete! Total responses: {current}")

if __name__ == "__main__":
    collector = DataCollector()
    collector.collect_all(
        csv_path="data/prompts/prompts.csv",
        models=list(MODELS_GROQ.values())
    )