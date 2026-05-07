import os
import json
from collections import defaultdict
import pandas as pd

class BasicAnalyzer:
    def __init__(self):
        self.data = []
        
    def load_all_responses(self, response_dir="data/responses"):
        """Load all JSON files from model subfolders"""
        print("Loading response files...")
        
        for model_folder in os.listdir(response_dir):
            folder_path = os.path.join(response_dir, model_folder)
            if os.path.isdir(folder_path):
                for filename in os.listdir(folder_path):
                    if filename.endswith('.json'):
                        filepath = os.path.join(folder_path, filename)
                        try:
                            with open(filepath, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                self.data.append(data)
                        except Exception as e:
                            print(f"Error loading {filename}: {e}")
        
        print(f"Loaded {len(self.data)} responses")
        return self.data
    
    def basic_statistics(self):
        """Basic statistics"""
        stats = {
            'total': len(self.data),
            'by_model': defaultdict(int),
            'by_category': defaultdict(int),
            'success': 0,
            'errors': 0,
            'forbidden_403': 0
        }
        
        for item in self.data:
            model = item.get('model', 'unknown')
            category = item.get('category', 'unknown')
            
            stats['by_model'][model] += 1
            stats['by_category'][category] += 1
            
            if item.get('error'):
                stats['errors'] += 1
                if '403' in str(item['error']) or 'Forbidden' in str(item['error']):
                    stats['forbidden_403'] += 1
            else:
                stats['success'] += 1
        
        return stats
    
    def print_statistics(self, stats):
        """Print statistics"""
        print("\n" + "="*50)
        print("BASIC STATISTICS")
        print("="*50)
        
        print(f"\nTotal responses: {stats['total']}")
        print(f"Successful: {stats['success']} ({stats['success']/stats['total']*100:.1f}%)")
        print(f"Errors: {stats['errors']} ({stats['errors']/stats['total']*100:.1f}%)")
        print(f"  - 403 Forbidden: {stats['forbidden_403']}")
        
        print("\n--- BY MODEL ---")
        for model, count in sorted(stats['by_model'].items()):
            print(f"{model}: {count}")
        
        print("\n--- BY CATEGORY ---")
        for category, count in sorted(stats['by_category'].items()):
            print(f"{category}: {count}")
    
    def create_dataframe(self):
        """Create pandas DataFrame"""
        rows = []
        
        for item in self.data:
            row = {
                'prompt_id': item.get('prompt_id'),
                'category': item.get('category'),
                'subcategory': item.get('subcategory'),
                'sensitivity_level': item.get('sensitivity_level'),
                'model': item.get('model'),
                'has_response': item.get('response') is not None,
                'has_error': item.get('error') is not None,
                'is_403': '403' in str(item.get('error', '')) or 'Forbidden' in str(item.get('error', '')),
                'response_length': len(item.get('response', '').split()) if item.get('response') else 0,
                'response_text': item.get('response', '')
            }
            rows.append(row)
        
        df = pd.DataFrame(rows)
        return df
    
    def save_dataframe(self, df, filename="data/analysis/responses_dataset.csv"):
        """Save to CSV"""
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"\nDataFrame saved to {filename}")


if __name__ == "__main__":
    analyzer = BasicAnalyzer()
    analyzer.load_all_responses()
    stats = analyzer.basic_statistics()
    analyzer.print_statistics(stats)
    df = analyzer.create_dataframe()
    analyzer.save_dataframe(df)
    print("\nBasic analysis complete!")