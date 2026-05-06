import os
from collect_data import DataCollector
from config import MODELS

def get_completed():
    """Find already collected prompt+model combinations"""
    completed = set()
    response_dir = "data/responses"
    
    if not os.path.exists(response_dir):
        return completed
    
    for filename in os.listdir(response_dir):
        if filename.endswith('.json'):
            # Remove .json extension
            name = filename.replace('.json', '')
            # Format: prompt_1_gpt-oss-120b:free
            # Split only on first underscore after 'prompt'
            parts = name.split('_', 2)  # ['prompt', '1', 'gpt-oss-120b:free']
            if len(parts) >= 3:
                prompt_id = parts[1]
                model_part = parts[2]
                completed.add(f"{prompt_id}_{model_part}")
    
    return completed

def resume_collection():
    """Continue collection from where it stopped"""
    collector = DataCollector()
    prompts = collector.load_prompts("data/prompts/prompts.csv")
    models = list(MODELS.values())
    
    completed = get_completed()
    print(f"Already completed: {len(completed)} responses")
    
    # Find what's missing
    missing = []
    for prompt in prompts:
        for model in models:
            model_name = model.split('/')[-1]
            key = f"{prompt['id']}_{model_name}"
            if key not in completed:
                missing.append((prompt, model))
    
    print(f"Missing responses: {len(missing)}")
    print(f"Starting from where we left off...\n")
    
    if not missing:
        print("All responses already collected!")
        return
    
    import time
    total = len(missing)
    for i, (prompt, model) in enumerate(missing):
        print(f"[{i+1}/{total}] Prompt {prompt['id']} - {model}")
        response = collector.query_model(model, prompt['prompt'])
        collector.save_response(prompt, model, response)
        
        if response['success']:
            print(f"Success: {response['response'][:80]}...")
        else:
            print(f"Error: {response['error']}")
        
        if "gpt-oss" in model:
            time.sleep(15)
        else:
            time.sleep(5)
    
    print(f"\nDone! Collected {total} missing responses.")

if __name__ == "__main__":
    resume_collection()