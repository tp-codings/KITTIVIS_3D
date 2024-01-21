import numpy as np
import argparse
import os

def read_bin(file_path):
    points = np.fromfile(file_path, dtype=np.float32)
    points = points.reshape((-1, 4))  # Angenommen: Punkte haben 4 Werte (x, y, z, Intensität)
    return points

def save_bin(points, file_path):
    points.astype(np.float32).tofile(file_path)

def calculate_angle(z, xy):
    """Berechnet den vertikalen Winkel des Punktes."""
    return np.arctan2(z, xy) * 180 / np.pi

def filter_layers(points, step, num_layers=64):
    """Entfernt jeden 'step'-ten Layer aus der Punktwolke."""
    xy_distances = np.sqrt(points[:, 0]**2 + points[:, 1]**2)
    angles = calculate_angle(points[:, 2], xy_distances)

    # Klassifizieren der Winkel in Bins, die den Layern entsprechen (64 Layer im Winkel von -24.8 bis +2 (siehe Datenblatt https://hypertech.co.il/wp-content/uploads/2015/12/HDL-64E-Data-Sheet.pdf))
    bins = np.linspace(-24.8, 2, num=num_layers+1)
    layer_indices = np.digitize(angles, bins) - 1

    # Filtern der Layer
    return points[layer_indices % step != 0]

def process_files(input_folder, step, output_folder_name):
    output_folder = os.path.join(input_folder, output_folder_name)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.endswith('.bin'):
            input_file = os.path.join(input_folder, file_name)
            output_file = os.path.join(output_folder, file_name)

            points = read_bin(input_file)
            filtered_points = filter_layers(points, step)
            save_bin(filtered_points, output_file)

# Argument Parser Setup
parser = argparse.ArgumentParser(description='Filtert Layers in Punktwolken von Velodyne-Scannern.')
parser.add_argument('--input_folder', type=str, help='Pfad zum Eingabeordner')
parser.add_argument('--step', type=int, default=2, help='Filtergrad (jeder x-te Layer wird entfernt)')
parser.add_argument('--folder_name', default="data_layer_reduced_x", help='Name des Ausgabeordners')

args = parser.parse_args()

if args.folder_name == "data_layer_reduced_x":
    folder_name = args.folder_name + str(args.step)
else:
    folder_name = args.folder_name

process_files(args.input_folder, args.step, folder_name)
