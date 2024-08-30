import pandas as pd
import scikit_posthocs as sp

# Step 1: Load data from Excel file
df = pd.read_csv('rq1\\best_configuration\\analysis\\all_configs.csv')

# Step 2: Prepare data for the Nemenyi test
# Create a pivot table where rows are repositories and columns are configs
pivot_df = df.pivot(index='repository', columns='config', values='mcc')

# Convert the pivot table to numpy array for processing
data = pivot_df.to_numpy()

# Step 3: Apply the Nemenyi test using scikit-posthocs
nemenyi_results = sp.posthoc_nemenyi_friedman(data)

# Display the results
print(nemenyi_results)


df = pd.read_csv('rq1\\best_configuration\\config_statistic_comparison\\nemenyi_rank.csv')
avg_ranks = df.groupby('config')['rank'].mean()
print("Average Rank:")
print(avg_ranks)