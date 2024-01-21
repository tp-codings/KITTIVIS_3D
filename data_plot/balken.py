import pandas as pd
import matplotlib.pyplot as plt
from data_source import data

df = pd.DataFrame(data)
df_melted = df.melt(id_vars="Method", var_name="Category", value_name="Score")
df_melted[['Vehicle', 'Difficulty']] = df_melted['Category'].str.rsplit('_', n=1, expand=True)

fig, ax = plt.subplots(figsize=(15, 8))

colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

for i, difficulty in enumerate(df_melted['Difficulty'].unique()):
    subset = df_melted[df_melted['Difficulty'] == difficulty]
    ax.bar(subset['Method'], subset['Score'], color=colors[i], width=0.2, label=difficulty, align='center')

ax.set_xticklabels(df['Method'], rotation=45, ha='right')

ax.legend(title="Difficulty")

ax.set_xlabel('Method')
ax.set_ylabel('Score')
ax.set_title('Scores by Method and Difficulty')

plt.tight_layout()
plt.show()
