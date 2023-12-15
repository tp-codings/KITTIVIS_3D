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

_seq = "data/0071"

base_directory = _seq