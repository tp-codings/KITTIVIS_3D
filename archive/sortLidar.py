import numpy as np

def read_kitti_point_cloud(file_path):
    """ Einlesen einer KITTI-Punktwolkendatei. """
    point_cloud = np.fromfile(file_path, dtype=np.float32)
    point_cloud = point_cloud.reshape((-1, 4))  # KITTI-Punktwolken haben 4 Werte pro Punkt (x, y, z, Intensität)
    return point_cloud

def sort_points_by_x(point_cloud):
    """ Sortiert die Punkte der Punktwolke nach dem X-Wert. """
    sorted_points = point_cloud[point_cloud[:, 0].argsort()]  # Sortiert nach der ersten Spalte (X-Werte)
    return sorted_points

def save_kitti_point_cloud(point_cloud, file_path):
    """ Speichert die Punktwolke im KITTI-Format. """
    point_cloud.tofile(file_path)

# Pfad zur KITTI-Punktwolkendatei
input_file_path = r"D:\1. Programmieren\Python\KITTIVIS_3D\data\0051\velodyne_points\source\0000000000.bin"
output_file_path = r"D:\1. Programmieren\Python\KITTIVIS_3D\data\0051\velodyne_points\source\0000000001.bin"

# Einlesen und Sortieren der Punktwolke
point_cloud = read_kitti_point_cloud(input_file_path)
sorted_point_cloud = sort_points_by_x(point_cloud)

# Speichern der sortierten Punktwolke
save_kitti_point_cloud(sorted_point_cloud, output_file_path)

print(f"Sortierte Punktwolke gespeichert unter: {output_file_path}")
