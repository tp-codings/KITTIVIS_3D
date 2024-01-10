def keep_lines_under_limit(file_path, x, y):
    """
    Behält nur die ersten x Zeilen der angegebenen Datei, vorausgesetzt, der Wert in jeder Zeile ist kleiner als y.

    :param file_path: Pfad zur Textdatei.
    :param x: Maximale Anzahl der zu behaltenden Zeilen.
    :param y: Grenzwert, unter dem der Wert in der Zeile liegen muss.
    """
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Filtere und behalte nur Zeilen, deren Wert kleiner als y ist, bis zu x Zeilen
        filtered_lines = [line for line in lines if int(line.strip()) < y][:x]

        with open(file_path, 'w') as file:
            file.writelines(filtered_lines)

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

# Beispiel der Verwendung:
path = r"E:\ML\PointPillars\dataset\ImageSets\val.txt"
keep_lines_under_limit(path, 2462, 2462)
