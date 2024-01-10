import os

def remove_last_entry(line):
    entries = line.split()
    if entries:
        entries.pop()
    return ' '.join(entries)

def remove_last_entry_from_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)

            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            modified_lines = [remove_last_entry(line) for line in lines]

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write('\n'.join(modified_lines))

# Beispiel: Ordnerpfad anpassen
folder_path = r"E:\ML_Datasets\nuScenes\Test\reicht\training\label_2"
remove_last_entry_from_files(folder_path)
