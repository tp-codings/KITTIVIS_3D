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

min_tresh = 0.3

#0000000000
#000000

start_frame = "0000000000"

_seq = "data/source"

ckpt = "pillar_logs/checkpoints/PP_MOF_160.pth"

base_directory = _seq