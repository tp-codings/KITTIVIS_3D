import os

def process_file(file_path):

    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            if line.lower().startswith('pedestrian'):
                file.write('Pedestrian' + line[10:])  # Preserving the rest of the line
            elif line.lower().startswith('bicycle') or line.lower().startswith('cyclist'):
                file.write('Cyclist' + line[7:])     # Converting 'bicycle' to 'cyclist'
            elif line.lower().startswith('car'):
                file.write('Car' + line[3:] )         # Preserving the rest of the line
        file.write('\n')

def process_directory(directory_path):

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path) and file_path.endswith('.txt'):
            process_file(file_path)

directory_path = r"E:\ML_Datasets\nuScenes\Test\lastHope\training\label_2"
process_directory(directory_path)
