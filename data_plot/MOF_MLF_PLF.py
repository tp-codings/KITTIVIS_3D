import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = {
    'Pedestrian': {
        'MOF -> POF': [51.45, 47.97, 43.84],
        'MOF -> PLF': [39.48, 37.56, 33.59],
    },
    'Cyclist': {
        'MOF -> POF': [81.88, 63.67, 60.90],
        'MOF -> PLF': [74.19, 52.89, 49.37],
    },
    'Car': {
        'MOF -> POF': [86.64, 76.75, 74.17],
        'MOF -> PLF': [83.10, 66.45, 58.64],
    }
}

df = pd.DataFrame(data)

difficulty_levels = ['Easy', 'Moderate', 'Hard']

percentage_diff_df = pd.DataFrame({
    category: {
        'Easy': data[category]['MOF -> POF'][0] - data[category]['MOF -> PLF'][0],
        'Moderate': data[category]['MOF -> POF'][1] - data[category]['MOF -> PLF'][1],
        'Hard': data[category]['MOF -> POF'][2] - data[category]['MOF -> PLF'][2]
    } for category in data
}).T

colors = {
    'MOF -> POF': 'darkblue',
    'MOF -> PLF': '#800000',
    'Difference': 'darkgreen'
}

fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 6))

axes[0].set_ylabel('Score')


for idx, (category, ax) in enumerate(zip(df.columns, axes)):
    ax.plot(difficulty_levels, df[category]['MOF -> POF'], marker='o', label='MOF -> POF', color=colors['MOF -> POF'])
    ax.plot(difficulty_levels, df[category]['MOF -> PLF'], marker='x', linestyle='--', label='MOF -> PLF', color=colors['MOF -> PLF'])
    
    for i, diff in enumerate(percentage_diff_df.loc[category]):
        ax.text(i, (df[category]['MOF -> POF'][i] + df[category]['MOF -> PLF'][i]) / 2, 
                f'{diff:.2f}%', ha='center', va='bottom', color=colors['Difference'])
    
    ax.set_title(category)
    ax.legend()

plt.tight_layout()
plt.show()


#------------------------------------------------------------------------------------------------------------------------------------
from data_source import data_trans as data


# Convert the mock data to a DataFrame
data = pd.DataFrame(data)
data.set_index('Transfer', inplace=True)

# Extract the scores for MOF -> PLF and MLF -> PLF
mof_PLF = data.loc['MOF -> PLF']
MLF_PLF = data.loc['MLF -> PLF']

# Categories and difficulties
categories = ['Pedestrian', 'Cyclist', 'Car']
difficulties = ['Easy', 'Moderate', 'Hard']

# Scores for each category and difficulty
mof_PLF_scores = [mof_PLF[f'{cat}_{diff}'] for cat in categories for diff in difficulties]
MLF_PLF_scores = [MLF_PLF[f'{cat}_{diff}'] for cat in categories for diff in difficulties]

# Colors for the bars
color_mof_PLF = '#800000'
color_MLF_PLF = '#400000'

# Create subplots for each category
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 6), sharey=True)

# Define the bar width and the index for the bars
bar_width = 0.35
index = np.arange(len(difficulties))

# Loop through each category and create the bar plots
for idx, cat in enumerate(categories):
    axes[idx].bar(index, mof_PLF_scores[idx*3:(idx+1)*3], bar_width, label='MOF -> PLF', color=color_mof_PLF)
    axes[idx].bar(index + bar_width, MLF_PLF_scores[idx*3:(idx+1)*3], bar_width, label='MLF -> PLF', color=color_MLF_PLF)
    
    axes[idx].set_title(cat)
    axes[idx].set_xticks(index + bar_width / 2)
    axes[idx].set_xticklabels(difficulties)
    axes[idx].legend()

#fig.suptitle('Vergleich der Scores zwischen MOF -> PLF und MLF -> PLF')
axes[0].set_ylabel('Score')


# Add the annotations for each bar
for ax in axes:
    for bar in ax.patches:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  
                    textcoords='offset points',
                    ha='center', va='bottom')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Adjust the layout to make room for the common labels
plt.show()

