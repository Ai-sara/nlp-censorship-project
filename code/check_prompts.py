import pandas as pd

df = pd.read_csv('data/prompts/prompts.csv')

print(f"Total prompts: {len(df)}")
print()
print("By category:")
print(df['category'].value_counts())
print()
print("By sensitivity level:")
print(df['sensitivity_level'].value_counts())
print()
print("By expected response:")
print(df['expected_response'].value_counts())