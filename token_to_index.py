import os

def rename_files_in_folder(folder_path):
    # Liste alle Dateien im Verzeichnis auf
    files = sorted(os.listdir(folder_path))

    # Zähler für die Benennung der Dateien
    counter = 0

    for file in files:
        # Erstelle den neuen Dateinamen
        new_file_name = f"{counter:06d}{os.path.splitext(file)[1]}"

        # Pfad der alten und neuen Datei
        old_file_path = os.path.join(folder_path, file)
        new_file_path = os.path.join(folder_path, new_file_name)

        # Umbenennen der Datei
        os.rename(old_file_path, new_file_path)

        # Zähler erhöhen
        counter += 1

    print(f"{counter} Dateien wurden umbenannt.")

# Pfad zum Ordner angeben
folder_path = r"E:\ML_Datasets\nuScenes\Test\lastHope\train\calib"
rename_files_in_folder(folder_path)
