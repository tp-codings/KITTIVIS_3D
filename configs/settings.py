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

min_tresh = 0.6

_seq = "data/0051"

ckpt = "pillar_logs/checkpoints/PP_MSF_160.pth"

base_directory = _seq