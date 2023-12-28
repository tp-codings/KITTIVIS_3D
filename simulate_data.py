import os
import shutil
import signal
import time
import argparse
from tqdm import tqdm
import time
from utils.utilities import incrementString
import keyboard

def check_folders_existence(cam_paths, oxts_path, tracklets_path, velodyne_path):
    existence = [True, True, True, True]
    # Check camera paths
    for cam_path in cam_paths:
        if not os.path.exists(cam_path):
            add_output(f"The folder {cam_path} does not exist.")
            existence[0] = False

    # Check oxts path
    if not os.path.exists(oxts_path):
        add_output(f"The folder {oxts_path} does not exist.")
        existence[1] = False

    # Check tracklets path
    if not os.path.exists(tracklets_path):
        add_output(f"The folder {tracklets_path} does not exist.")
        existence[2] = False

    # Check velodyne path
    if not os.path.exists(velodyne_path):
        add_output(f"The folder {velodyne_path} does not exist.")
        existence[3] = False

    return existence

def copy_file(base_path, current_frame, ending, filter = "data"):
    target_path = os.path.join(base_path, "source")
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    data_path = os.path.join(base_path, filter, current_frame + ending)
    target_path = os.path.join(target_path)

    if not os.path.exists(data_path):
        add_output(f"no data at: {data_path}")
    else:
        shutil.copy(data_path, target_path)
        add_output(f"Copied: {data_path} to {target_path}")

def on_exit(signum, frame):
    global output
    output = ""
    add_output("Program ended. Cleaning up data...")

    for cam_path in cam_paths:
        file_path = os.path.join(cam_path, "source")
        if os.path.exists(file_path):
            shutil.rmtree(file_path)
            add_output(f"Data at {file_path} has been deleted.")

    file_path = os.path.join(oxts_path, "source")
    if os.path.exists(file_path):
        shutil.rmtree(file_path)
        add_output(f"Data at {file_path} has been deleted.")

    file_path = os.path.join(tracklets_path, "source")
    if os.path.exists(file_path):
        shutil.rmtree(file_path)
        add_output(f"Data at {file_path} has been deleted.")

    file_path = os.path.join(velodyne_path, "source")
    if os.path.exists(file_path):
        shutil.rmtree(file_path)
        add_output(f"Data at {file_path} has been deleted.")

    add_output("Data cleanup complete.")
    print_output(output)
    progress_bar.close()
    exit()

def add_output(message):
    global output
    output = output + str(message) + '\n'

def print_output(output):
    global progress_bar
    os.system('cls')
    print(output)
    progress_bar.update(1)

global pause
pause = False

if __name__ == "__main__":
    global output, progress_bar
    output = ""
    
    parser = argparse.ArgumentParser(description="Simulate realtime data by moving files from data to source (img0-3, oxts, tracklets, velodyne_points)")
    parser.add_argument("--folder_path", help="Path to data folder", default = "Live/data")
    parser.add_argument("--time_step", help="Time step between frames", default= 1.0, type=float)
    parser.add_argument("--mode", help="FPF (Frame Per Frame) or default", default = "default")
    parser.add_argument("--filter", help="Option for selecting folder with filtered pointcloud", default = "data")
    args = parser.parse_args()

    base_dir = args.folder_path
    time_step = args.time_step
    mode = args.mode
    filter_sys = args.filter

    cam_paths = [os.path.join(base_dir, f"image_{i:02d}") for i in range(0, 4)]
    oxts_path = os.path.join(base_dir, "oxts")
    tracklets_path = os.path.join(base_dir, "tracklets")
    velodyne_path = os.path.join(base_dir, "velodyne_points")

    existence = check_folders_existence(cam_paths, oxts_path, tracklets_path, velodyne_path)

    cam_data = []
    oxts_data = None
    tracklets_data = None
    velodyne_data = None

    if existence[0] == True:
        for cam in cam_paths:
            file_path = os.path.join(cam, "data")
            if os.path.exists(file_path):
                cam_data.append(file_path)
            else:
                add_output(f"no data at: {file_path}")

    if existence[1] == True:
        file_path = os.path.join(oxts_path, "data")
        if os.path.exists(file_path):
            oxts_data = file_path
        else:
            add_output(f"no data at: {file_path}")

    if existence[2] == True:
        file_path = os.path.join(tracklets_path, "data")
        if os.path.exists(file_path):
            tracklets_data = file_path
        else:
            add_output(f"no data at: {file_path}")

    if existence[3] == True:
        file_path = os.path.join(velodyne_path, filter_sys)
        if os.path.exists(file_path):
            velodyne_data = file_path
        else:
            add_output("no data at: {file_path}")

    current_frame = "0000000000"
    max_frames = 0

    if velodyne_data is not None:
        items = os.listdir(velodyne_data)
        max_frames = len(items) - 1

    progress_bar = tqdm(total=max_frames,  position=0, desc='Processing Frames', unit='frames')
    add_output(max_frames)
    frame_index = 0

    # Add signal handlers for program termination
    signal.signal(signal.SIGINT, on_exit)
    signal.signal(signal.SIGTERM, on_exit)


    while True:
        output = ""
        
        if mode == "FPF":
            keyboard.wait('space')
        elif mode == "default":
            if not pause:
                if keyboard.is_pressed('space'):
                    pause = True
            else:
                keyboard.wait('space')
                pause = False


        try:
            if cam_data is not None:
                for i, path in enumerate(cam_paths):
                    copy_file(path, current_frame, ".png")

            if oxts_data is not None:
                copy_file(oxts_path, current_frame, ".txt")

            if tracklets_data is not None:
                copy_file(tracklets_path, current_frame, ".txt")

            if velodyne_data is not None:
                copy_file(velodyne_path, current_frame, ".bin", filter=filter_sys)

            current_frame = incrementString(current_frame)
            frame_index += 1

            add_output(f"{round(frame_index/max_frames * 100, 2)}%")
            print_output(output)
            time.sleep(time_step)  # One second pause between files

        except Exception as e:
            add_output(f"An error occurred: {str(e)}")
