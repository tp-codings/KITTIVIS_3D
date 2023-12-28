import numpy as np
import argparse
import os

def read_bin(file_path):
    """Liest eine bin-Datei und gibt die Punktwolke zurück."""
    points = np.fromfile(file_path, dtype=np.float32)
    points = points.reshape((-1, 4))  # Annahme: Jeder Punkt hat 4 Werte (x, y, z, Intensität)
    return points

def save_bin(points, file_path):
    """Speichert die Punktwolke in einer bin-Datei."""
    points.astype(np.float32).tofile(file_path)

def filter_points(points, step):
    """Filtert die Punktwolke, indem jeder 'step'-te Punkt behalten wird."""
    return points[::step]

def process_files(input_folder, step, output_folder_name):
    output_folder = os.path.join(input_folder, output_folder_name)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    """Verarbeitet alle bin-Dateien im angegebenen Ordner."""
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.bin'):
            input_file = os.path.join(input_folder, file_name)
            output_file = os.path.join(output_folder, file_name)

            points = read_bin(input_file)
            filtered_points = filter_points(points, step)
            save_bin(filtered_points, output_file)

# Argument Parser Setup
parser = argparse.ArgumentParser(description='Filtert Punktwolken in bin-Dateien.')
parser.add_argument('--input_folder', type=str, help='Pfad zum Eingabeordner')
parser.add_argument('--step', type=int, default=2, help='Filtergrad (jeder x-te Punkt wird behalten)')
parser.add_argument('--folder_name', default="data_sys_reduced_x", help='Name of output folder')

# Parse arguments
args = parser.parse_args()

if args.folder_name == "data_sys_reduced_x":
    folder_name = args.folder_name + str(args.step)
else:
    folder_name = args.folder_name

# Verarbeite die Dateien
process_files(args.input_folder, args.step, folder_name)
