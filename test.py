import re

def parse_quader_data(file_path):
    with open(file_path, 'r') as file:
        quader_data = file.readlines()

    types_list = []
    coordinates_list = []

    for line in quader_data:
        data = line.split()
        if len(data) < 24:
            continue  # Skip lines with incomplete data

        quader_type = data[0]

        types_list.append(quader_type)
        coordinates_list.append([
            [float(x) for x in data[1:9]],
            [float(x) for x in data[9:17]],
            [float(x) for x in data[17:25]]
        ])

    return types_list, coordinates_list

# Beispielaufruf:
file_path = 'data/Live/tracklets/0000000000.txt'
types_list, coordinates_list = parse_quader_data(file_path)

print(types_list)
print(coordinates_list)

# Ausgabe der Ergebnisse
# for i, quader_type in enumerate(types_list):
#     print(f'Typ {i + 1}: {quader_type}')
#     print(f'Eckpunkte: {coordinates_list[i]}')
#     print('---')
