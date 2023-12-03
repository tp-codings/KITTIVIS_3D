from tqdm import tqdm
import time

max_frames = 100  # Beispielwert
frame_index = 0

# Erstelle eine Fortschrittsleiste mit der Gesamtanzahl der Frames
progress_bar = tqdm(total=max_frames, position=0, desc='Processing Frames', unit='frames')

while frame_index < max_frames:
    # Hier werden deine Verarbeitungsschritte durchgeführt
    time.sleep(0.1)  # Beispiel für Verarbeitungszeit

    # Aktualisiere die Fortschrittsleiste
    progress_bar.update(1)
    frame_index += 1

# Schließe die Fortschrittsleiste, wenn die Verarbeitung abgeschlossen ist
progress_bar.close()