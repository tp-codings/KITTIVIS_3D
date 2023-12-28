import numpy as np

def remove_ring_indices(input_file, output_file):
    # Lese die Daten aus der Datei
    data = np.fromfile(input_file, dtype=np.float32)

    # Überprüfe, ob die Länge der Daten ein Vielfaches von 5 ist (X, Y, Z, Intensität, Ring Index)
    if len(data) % 5 != 0:
        raise ValueError("Dateiformat ist nicht korrekt oder beschädigt.")

    # Forme das Array um, sodass jede Zeile einem Punkt entspricht
    reshaped_data = data.reshape(-1, 5)

    # Entferne die Spalte für den Ring Index (die fünfte Spalte)
    data_without_ring_index = reshaped_data[:, :4]

    # Schreibe die verbleibenden Daten in die Ausgabedatei
    data_without_ring_index.astype(np.float32).tofile(output_file)

# Verwendung des Skripts
input_filename = r"D:\1. Programmieren\Python\KITTIVIS_3D\data\0051\velodyne_points\source\0000000000.bin"
output_filename = r"D:\1. Programmieren\Python\KITTIVIS_3D\data\0051\velodyne_points\source\0000000000.bin"
remove_ring_indices(input_filename, output_filename)
