import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from data_source import data

df = pd.DataFrame(data)
df_melted = df.melt(id_vars="Method", var_name="Category", value_name="Score")
df_melted[['Vehicle', 'Difficulty']] = df_melted['Category'].str.rsplit('_', n=1, expand=True)

# Erstellen einer Farbpalette basierend auf der Anzahl der Methoden
palette = sns.color_palette("hsv", len(df_melted['Method'].unique()))

plt.figure(figsize=(18, 10))

# Anwenden der Farbpalette auf jeden Boxplot
plt.subplot(3, 1, 1)
sns.boxplot(x='Method', y='Score', data=df_melted[df_melted['Vehicle'] == 'Pedestrian'], showfliers=False, palette=palette)
plt.title('Pedestrian Scores Distribution by Method')
plt.xlabel('')
plt.ylabel('Score')

plt.subplot(3, 1, 2)
sns.boxplot(x='Method', y='Score', data=df_melted[df_melted['Vehicle'] == 'Cyclist'], showfliers=False, palette=palette)
plt.title('Cyclist Scores Distribution by Method')
plt.xlabel('')
plt.ylabel('Score')

plt.subplot(3, 1, 3)
sns.boxplot(x='Method', y='Score', data=df_melted[df_melted['Vehicle'] == 'Car'], showfliers=False, palette=palette)
plt.title('Car Scores Distribution by Method')
plt.xlabel('Method')
plt.ylabel('Score')

plt.tight_layout()
plt.show()
