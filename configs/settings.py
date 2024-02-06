import os

colors = {
    'car': (0.0, 0.0, 1.0),  # Blau
    'tram': (1.0, 0.0, 0.0),  # Rot
    'cyclist': (0.0, 1.0, 0.0),  # Grün
    'van': (0.0, 1.0, 1.0),  # Cyan
    'truck': (1.0, 0.0, 1.0),  # Magenta
    'pedestrian': (1.0, 1.0, 0.0),  # Gelb
    'sitter': (0.0, 0.0, 0.0),  # Schwarz
    'misc' : (0.0, 0.4, 1.0)
}
colors_gt = {
    'car': (0.0, 0.5, 1.0),       # Intensiveres Türkis
    'tram': (1.0, 0.5, 0.5),       # Deutlicheres Pink
    'cyclist': (0.5, 1.0, 0.0),    # Sehr helles Grün
    'van': (0.0, 1.0, 1.0),        # Cyan (unverändert)
    'truck': (1.0, 0.5, 1.0),      # Sehr helles Magenta
    'pedestrian': (1.0, 1.0, 0.0), # Starkes Orange
    'sitter': (0.0, 0.0, 0.0),     # Schwarz (unverändert)
    'misc': (0.0, 1.0, 1.0)        # Sehr lebhaftes Türkis
}

min_tresh = 0.5

#0000000000
#000000

start_frame = "0000000000"

_seq = "data/source"

ckpt = "weights/PP_MOF_160.pth"

base_directory = _seq