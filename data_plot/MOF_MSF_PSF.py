import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = {
    'Pedestrian': {
        'MOF -> POF': [51.45, 47.97, 43.84],
        'MOF -> PSF': [42.44, 39.05, 35.05],
    },
    'Cyclist': {
        'MOF -> POF': [81.88, 63.67, 60.90],
        'MOF -> PSF': [73.02, 53.43, 50.19],
    },
    'Car': {
        'MOF -> POF': [86.64, 76.75, 74.17],
        'MOF -> PSF': [83.67, 68.67, 66.73],
    }
}

df = pd.DataFrame(data)

difficulty_levels = ['Easy', 'Moderate', 'Hard']

percentage_diff_df = pd.DataFrame({
    category: {
        'Easy': 100 * (data[category]['MOF -> POF'][0] - data[category]['MOF -> PSF'][0]) / data[category]['MOF -> PSF'][0],
        'Moderate': 100 * (data[category]['MOF -> POF'][1] - data[category]['MOF -> PSF'][1]) / data[category]['MOF -> PSF'][1],
        'Hard': 100 * (data[category]['MOF -> POF'][2] - data[category]['MOF -> PSF'][2]) / data[category]['MOF -> PSF'][2]
    } for category in data
}).T

colors = {
    'MOF -> POF': 'darkblue',
    'MOF -> PSF': '#80A897',
    'Difference': 'darkgreen'
}

fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 6))

axes[0].set_ylabel('Score')


for idx, (category, ax) in enumerate(zip(df.columns, axes)):
    ax.plot(difficulty_levels, df[category]['MOF -> POF'], marker='o', label='MOF -> POF', color=colors['MOF -> POF'])
    ax.plot(difficulty_levels, df[category]['MOF -> PSF'], marker='x', linestyle='--', label='MOF -> PSF', color=colors['MOF -> PSF'])
    
    for i, diff in enumerate(percentage_diff_df.loc[category]):
        ax.text(i, (df[category]['MOF -> POF'][i] + df[category]['MOF -> PSF'][i]) / 2, 
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

# Extract the scores for MOF -> PSF and MSF -> PSF
mof_psf = data.loc['MOF -> PSF']
msf_psf = data.loc['MSF -> PSF']

# Categories and difficulties
categories = ['Pedestrian', 'Cyclist', 'Car']
difficulties = ['Easy', 'Moderate', 'Hard']

# Scores for each category and difficulty
mof_psf_scores = [mof_psf[f'{cat}_{diff}'] for cat in categories for diff in difficulties]
msf_psf_scores = [msf_psf[f'{cat}_{diff}'] for cat in categories for diff in difficulties]

# Colors for the bars
color_mof_psf = '#80A897'
color_msf_psf = '#33493E'

# Create subplots for each category
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 6), sharey=True)

# Define the bar width and the index for the bars
bar_width = 0.35
index = np.arange(len(difficulties))

# Loop through each category and create the bar plots
for idx, cat in enumerate(categories):
    axes[idx].bar(index, mof_psf_scores[idx*3:(idx+1)*3], bar_width, label='MOF -> PSF', color=color_mof_psf)
    axes[idx].bar(index + bar_width, msf_psf_scores[idx*3:(idx+1)*3], bar_width, label='MSF -> PSF', color=color_msf_psf)
    
    axes[idx].set_title(cat)
    axes[idx].set_xticks(index + bar_width / 2)
    axes[idx].set_xticklabels(difficulties)
    axes[idx].legend()

#fig.suptitle('Vergleich der Scores zwischen MOF -> PSF und MSF -> PSF')
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

