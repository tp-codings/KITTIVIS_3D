import os
import shutil
import signal
import time
import argparse

def move_files_source_target(data_folder, target_folder):
    try:
        # List of files in the source folder
        files = os.listdir(data_folder)

        # Check if the source folder contains files
        if files:
            # Move files from source folder to target folder
            for file in files:
                source_path = os.path.join(data_folder, file)
                target_path = os.path.join(target_folder, file)
                
                shutil.copy(source_path, target_path)
                print(f"Copied: {source_path} to {target_path}")
                
                time.sleep(1.0)  # One second pause between files
        else:
            print("Source folder is empty.")

    except Exception as e:
        print(f"Error while copying: {str(e)}")

def on_exit(signum, frame):
    print("Program ended. Cleaning up data...")
    # You can implement the deletion process here
    files_in_target = os.listdir(target_folder)
    for file_in_target in files_in_target:
        file_path_in_target = os.path.join(target_folder, file_in_target)
        os.remove(file_path_in_target)
        print(f"Deleted: {file_path_in_target}")

    print("Data in the target folder has been deleted.")
    print("Data cleanup complete.")
    exit()

if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description="Move files from data folder to target folder.")

    # Add arguments
    parser.add_argument("--data_folder", help="Path to the data folder")
    parser.add_argument("--target_folder", help="Path to the target folder")

    # Parse command-line arguments
    args = parser.parse_args()

    # Paths to source and target folders
    data_folder = args.data_folder
    target_folder = args.target_folder

    print(data_folder)
    print(target_folder)

    # Add signal handlers for program termination
    signal.signal(signal.SIGINT, on_exit)
    signal.signal(signal.SIGTERM, on_exit)

    # Infinite loop
    while True:
        move_files_source_target(data_folder, target_folder)
        time.sleep(1.0)  # One second pause before moving files again
