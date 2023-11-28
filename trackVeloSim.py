import os
import shutil
import time

def verschiebe_dateien_quelle_ziel(quellordner, zielordner):
    try:
        # Liste der Dateien im Quellordner
        dateien = os.listdir(quellordner)

        # Überprüfen, ob der Quellordner Dateien enthält
        if dateien:
            # Dateien von Quellordner nach Zielordner verschieben
            for datei in dateien:
                quellpfad = os.path.join(quellordner, datei)
                zielpfad = os.path.join(zielordner, datei)
                
                shutil.move(quellpfad, zielpfad)
                print(f"Verschoben: {quellpfad} nach {zielpfad}")
                
                time.sleep(0.1)  # Eine Sekunde Pause zwischen den Dateien
        else:
            print("Quellordner ist leer.")

    except Exception as e:
        print(f"Fehler beim Verschieben der Dateien: {str(e)}")

if __name__ == "__main__":
    # Pfade zu Quell- und Zielordnern
    quellordner = "data/Live/velodyne_points/wait"
    zielordner = "data/Live/velodyne_points/data"

    # Endlosschleife
    while True:
        verschiebe_dateien_quelle_ziel(quellordner, zielordner)
        time.sleep(0.1)  # Eine Sekunde Pause vor dem erneuten Verschieben
