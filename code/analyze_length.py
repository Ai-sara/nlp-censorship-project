import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

class LengthAnalyzer:
    def __init__(self, csv_path="data/analysis/responses_dataset.csv"):
        self.df = pd.read_csv(csv_path)
        # Remove errors for length analysis
        self.df_valid = self.df[~self.df['has_error']].copy()
    
    def length_statistics(self):
        """Response length statistics"""
        print("\n" + "="*50)
        print("RESPONSE LENGTH ANALYSIS")
        print("="*50)
        
        print("\n--- OVERALL ---")
        print(f"Mean: {self.df_valid['response_length'].mean():.1f} words")
        print(f"Median: {self.df_valid['response_length'].median():.1f} words")
        print(f"Std: {self.df_valid['response_length'].std():.1f} words")
        
        print("\n--- BY MODEL ---")
        model_stats = self.df_valid.groupby('model')['response_length'].agg(['mean', 'median', 'std'])
        print(model_stats.round(1))
        
        print("\n--- BY CATEGORY ---")
        cat_stats = self.df_valid.groupby('category')['response_length'].agg(['mean', 'median', 'std'])
        print(cat_stats.round(1))
    
    def plot_length_distribution(self):
        """Chart: length distribution by model"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        self.df_valid.boxplot(column='response_length', by='model', ax=ax)
        ax.set_ylabel('Response Length (words)')
        ax.set_xlabel('Model')
        ax.set_title('Response Length Distribution by Model')
        plt.suptitle('')  # Remove default title
        
        plt.tight_layout()
        plt.savefig('data/analysis/length_distribution.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: length_distribution.png")
        plt.show()
    
    def plot_length_by_sensitivity(self):
        """Chart: response length vs sensitivity level"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        sensitivity_order = ['low', 'medium', 'high', 'critical']
        
        sns.boxplot(
            data=self.df_valid,
            x='sensitivity_level',
            y='response_length',
            hue='model',
            order=sensitivity_order,
            ax=ax
        )
        
        ax.set_ylabel('Response Length (words)')
        ax.set_xlabel('Sensitivity Level')
        ax.set_title('Response Length by Sensitivity Level and Model')
        ax.legend(title='Model', bbox_to_anchor=(1.05, 1))
        
        plt.tight_layout()
        plt.savefig('data/analysis/length_by_sensitivity.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: length_by_sensitivity.png")
        plt.show()
    
    def statistical_test(self):
        """Statistical test for differences between models"""
        print("\n--- STATISTICAL SIGNIFICANCE ---")
        
        models = self.df_valid['model'].unique()
        
        # ANOVA
        groups = [self.df_valid[self.df_valid['model'] == m]['response_length'].values 
                  for m in models]
        
        f_stat, p_value = stats.f_oneway(*groups)
        
        print(f"ANOVA F-statistic: {f_stat:.2f}")
        print(f"p-value: {p_value:.4f}")
        
        if p_value < 0.05:
            print("✓ Differences between models are statistically significant (p < 0.05)")
        else:
            print("✗ No significant differences found")

if __name__ == "__main__":
    analyzer = LengthAnalyzer()
    
    # Statistics
    analyzer.length_statistics()
    
    # Charts
    analyzer.plot_length_distribution()
    analyzer.plot_length_by_sensitivity()
    
    # Statistics
    analyzer.statistical_test()
    
    print("\n✓ Length analysis complete!")