import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from data_source import data

df = pd.DataFrame(data)
df_melted = df.melt(id_vars="Method", var_name="Category", value_name="Score")
df_melted[['Vehicle', 'Difficulty']] = df_melted['Category'].str.rsplit('_', n=1, expand=True)

heatmap_data = df_melted.pivot(index="Method", columns="Category", values="Score")

methods_order = ["MOF -> POF", "MOF -> PSF", "MOF -> PLF", "MSF -> POF", "MSF -> PSF", "MLF -> POF", "MLF -> PLF"]
categories_order = ['Pedestrian_Easy', 'Pedestrian_Moderate', 'Pedestrian_Hard',
                    'Cyclist_Easy', 'Cyclist_Moderate', 'Cyclist_Hard',
                    'Car_Easy', 'Car_Moderate', 'Car_Hard']
heatmap_data = heatmap_data.reindex(methods_order, axis=0)
heatmap_data = heatmap_data.reindex(categories_order, axis=1)

plt.figure(figsize=(14, 8))
ax = sns.heatmap(heatmap_data, annot=True, fmt=".1f", linewidths=.5, cmap="YlGnBu")
ax.set_yticklabels(ax.get_yticklabels(), rotation=0)  # Setzt die y-Achsenbeschriftungen horizontal

plt.title('Score Heatmap by Method and Category')
plt.ylabel('Method')
plt.xlabel('Category')

plt.tight_layout()
plt.show()
