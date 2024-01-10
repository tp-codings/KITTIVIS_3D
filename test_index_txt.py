# Python-Skript zum Schreiben von Zahlen, beginnend bei 000000, in aufsteigender Reihenfolge in jede Zeile einer Textdatei

# Dateiname festlegen
filename = r"E:\ML\PointPillars\dataset\ImageSets\test.txt"

# Die Anzahl der zu schreibenden Zeilen festlegen
num_lines = 914  # Beispiel: 1000 Zeilen

# Datei öffnen und Zahlen schreiben
with open(filename, "w") as file:
    for i in range(num_lines):
        # Formatierung der Zahl mit führenden Nullen (6 Stellen)
        line = f"{i:06}\n"
        file.write(line)

filename