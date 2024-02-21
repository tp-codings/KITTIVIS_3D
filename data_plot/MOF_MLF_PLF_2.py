import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = {
    'Pedestrian': {
        'MLF -> PLF': [51.74, 44.89, 39.61],
        'MOF -> PLF': [39.48, 37.56, 33.59],
    },
    'Cyclist': {
        'MLF -> PLF': [78.79, 61.86, 58.18],
        'MOF -> PLF': [74.19, 52.89, 49.37],
    },
    'Car': {
        'MLF -> PLF': [84.37, 76.34, 68.82],
        'MOF -> PLF': [83.10, 66.45, 58.64],
    }
}

df = pd.DataFrame(data)

difficulty_levels = ['Easy', 'Moderate', 'Hard']

percentage_diff_df = pd.DataFrame({
    category: {
        'Easy': 100 * (data[category]['MLF -> PLF'][0] - data[category]['MOF -> PLF'][0]) / data[category]['MOF -> PLF'][0],
        'Moderate': 100 * (data[category]['MLF -> PLF'][1] - data[category]['MOF -> PLF'][1]) / data[category]['MOF -> PLF'][1],
        'Hard': 100 * (data[category]['MLF -> PLF'][2] - data[category]['MOF -> PLF'][2]) / data[category]['MOF -> PLF'][2]
    } for category in data
}).T

colors = {
    'MOF -> PLF': '#800000',
    'MLF -> PLF': '#400000',
    'Difference': 'darkgreen'
}

fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 6))

axes[0].set_ylabel('Score')


for idx, (category, ax) in enumerate(zip(df.columns, axes)):
    ax.plot(difficulty_levels, df[category]['MOF -> PLF'], marker='o', label='MOF -> PLF', color=colors['MOF -> PLF'])
    ax.plot(difficulty_levels, df[category]['MLF -> PLF'], marker='x', linestyle='--', label='MLF -> PLF', color=colors['MLF -> PLF'])
    
    for i, diff in enumerate(percentage_diff_df.loc[category]):
        ax.text(i, (df[category]['MOF -> PLF'][i] + df[category]['MLF -> PLF'][i]) / 2, 
                f'{diff:.2f}%', ha='center', va='bottom', color=colors['Difference'])
    
    ax.set_title(category)
    ax.legend()

plt.tight_layout()
plt.show()
