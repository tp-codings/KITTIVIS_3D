import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = {
    'Pedestrian': {
        'MOF -> PSF': [42.44, 39.05, 35.05],
        'MSF -> PSF': [54.38, 48.83, 44.71],
    },
    'Cyclist': {
        'MOF -> PSF': [73.02, 53.43, 50.19],
        'MSF -> PSF': [74.76, 56.72, 53.35],
    },
    'Car': {
        'MOF -> PSF': [83.67, 68.67, 66.73],
        'MSF -> PSF': [84.46, 73.67, 68.31],
    }
}

df = pd.DataFrame(data)

difficulty_levels = ['Easy', 'Moderate', 'Hard']

percentage_diff_df = pd.DataFrame({
    category: {
        'Easy': 100 * (data[category]['MSF -> PSF'][0] - data[category]['MOF -> PSF'][0]) / data[category]['MOF -> PSF'][0],
        'Moderate': 100 * (data[category]['MSF -> PSF'][1] - data[category]['MOF -> PSF'][1]) / data[category]['MOF -> PSF'][1],
        'Hard': 100 * (data[category]['MSF -> PSF'][2] - data[category]['MOF -> PSF'][2]) / data[category]['MOF -> PSF'][2]
    } for category in data
}).T

colors = {
    'MOF -> PSF': '#80A897',
    'MSF -> PSF': '#33493E',
    'Difference': 'darkgreen'
}

fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 6))

axes[0].set_ylabel('Score')


for idx, (category, ax) in enumerate(zip(df.columns, axes)):
    ax.plot(difficulty_levels, df[category]['MOF -> PSF'], marker='o', label='MOF -> PSF', color=colors['MOF -> PSF'])
    ax.plot(difficulty_levels, df[category]['MSF -> PSF'], marker='x', linestyle='--', label='MSF -> PSF', color=colors['MSF -> PSF'])
    
    for i, diff in enumerate(percentage_diff_df.loc[category]):
        ax.text(i, (df[category]['MOF -> PSF'][i] + df[category]['MSF -> PSF'][i]) / 2, 
                f'{diff:.2f}%', ha='center', va='bottom', color=colors['Difference'])
    
    ax.set_title(category)
    ax.legend()

plt.tight_layout()
plt.show()

