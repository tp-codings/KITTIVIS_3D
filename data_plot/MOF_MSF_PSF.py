import pandas as pd
import matplotlib.pyplot as plt
from data_source import data_MOF_MSF as data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Angenommen, 'data' ist bereits in deinem Skript definiert
# from data_source import data_MOF_MSF as data

# Erstellen eines DataFrame aus den Daten
df = pd.DataFrame(data)
df.set_index('Transfer', inplace=True)

# Extrahieren der Daten für "MOF -> PSF" und "MSF -> PSF"
mof_psf = df.loc['MOF -> PSF']
msf_psf = df.loc['MSF -> PSF']

# Vorbereitung der Daten zum Plotten
categories = ['Pedestrian', 'Cyclist', 'Car']
difficulties = ['Easy', 'Moderate', 'Hard']
mof_psf_scores = [mof_psf[f'{cat}_{diff}'] for cat in categories for diff in difficulties]
msf_psf_scores = [msf_psf[f'{cat}_{diff}'] for cat in categories for diff in difficulties]

# Plotten der Daten
fig, ax = plt.subplots(figsize=(12, 8))
bar_width = 0.35
index = np.arange(len(categories) * len(difficulties))

# Farben für die Balken
color_mof_psf = '#80A897'
color_msf_psf = '#33493E'

bar1 = ax.bar(index, mof_psf_scores, bar_width, label='MOF -> PSF', color=color_mof_psf)
bar2 = ax.bar(index + bar_width, msf_psf_scores, bar_width, label='MSF -> PSF', color=color_msf_psf)

# Hinzufügen von Text für Labels, Titel und Achsenmarkierungen
ax.set_xlabel('Kategorien und Schwierigkeiten')
ax.set_ylabel('Scores')
ax.set_title('Metriken und Schwierigkeiten')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels([f'{cat}_{diff}' for cat in categories for diff in difficulties], rotation=45)
ax.legend()

# Hinzufügen der numerischen Daten auf die Balken
for bars in [bar1, bar2]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 Punkte vertikaler Versatz
                    textcoords='offset points',
                    ha='center', va='bottom')

plt.tight_layout()
plt.show()
