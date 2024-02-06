import pandas as pd
import matplotlib.pyplot as plt
from data_source import data_overview as data

colors = ['#80A897', '#800000', 'green', 'purple'] 

df = pd.DataFrame(data)
df.set_index('Method', inplace=True)

difficulties = ['Easy', 'Moderate', 'Hard']

fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)

for i, object_category in enumerate(['Pedestrian', 'Cyclist', 'Car']):
    for j, method in enumerate(df.index):
        axes[i].plot(difficulties, 
                     [df.loc[method, f'{object_category}_{diff}'] for diff in difficulties], 
                     marker='o', 
                     label=method,
                     color=colors[j]) 
        
    axes[i].set_title(f'{object_category}')
    axes[i].set_xticks(difficulties)
    axes[i].legend()
    axes[i].grid(True)

axes[0].set_ylabel('Score')

plt.tight_layout()
plt.show()
