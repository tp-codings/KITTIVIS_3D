# KITTIVIS_3D
This is a prototype for an interactive LiDAR visualization tool for primary KITTI scene data (protoype for nuScenes data included aswell). It should also serve as the basis for the development of a live-on-board system. An 3D object detection was implemented based on the PointPillars method.

## Features
- Real time interactive data visualization for sensor data in KITTI format
- Real time 3D object detection
- Converter for nuScenes -> KITTI (only for visualization)
- Environment for training and evaluating models
  
| Personal Rating | Year of Development | Languages | Tools | Type of Application |
| --- | --- | --- | --- | --- |
| ⭐️⭐️⭐️⭐️⭐️ (5/5) | 2024 | Python | OpenGL, PyGame, CUDA, PyTorch | Visualisierung |

# Getting Started 
## Prerequisites
- Python Version: 3.8
- Cuda Version: 12.1
- CuDNN Version: 12.x
- PyTorch Version: 2.1.1

## Installation
1. Clone Repository
`git clone https://github.com/tp-codings/KITTIVIS_3D.git`
2. Create Conda Environment
`conda create -n "KITTIVIS3D" python=3.8`
`conda activate KITTIVIS3D`
4. Install Pytorch 2.1.1
`pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121`
5. Install Dependencies (created with pipreqs)
`pip install -r requirements.txt`

# Usage
## Quick start
1. `python main.py`
2. `python simulate_data.py --folder_path "\data\kitti\0051 --time_step 0.1 --mode "default" --filter "data"`
3. Use the left mouse button to rotate around the origin.
4. Use the scroll wheel to zoom.

## Main visualization tool: main.py
The main.py is responsible for the interactive visualization of sensor data and the inference results of object detection. 
It is capable of visualizing data following the KITTI format. In this repository, a snippet of a KITTI scene and a converted nuScenes scene are included for testing purposes.

### Architecture
The application retrieves the data to be visualized from the directory /data/source/*. If no image is displayed, it means there are no data available in this directory. The data can be simulated using the script simulate_data.py (further described below).
The following image depicts the general architecture of the visualization tool following the update-render-pattern known from video games:

![architecture](https://github.com/tp-codings/KITTIVIS_3D/assets/118997294/4eaba372-c658-408b-a3c9-d2d9561b5585)

### Toggle components
The main.py contains the game loop, in which components can be toggled on and off by commenting. No UI has been developed for this purpose, but it can easily be integrated into the architecture using various conditions triggered by potential buttons. This script only needs to be executed and has no additional parameters. 

### Change model for object detection
In /configs/settings.py, you can set the path to the checkpoint file to be used for object detection.

## Data simulation: simulate_data.py
This script simulates the provisioning of sensor data using a simple copy procedure (img0-3, oxts, tracklets, velodyne_points).

### Parameter
- `-h, --help`:                  Show this help message and exit.
- `--folder_path FOLDER_PATH`:   Path to the data folder.
- `--time_step TIME_STEP`:       Time step between frames in seconds, simulating the operation speed of the sensor (default 1s) .
- `--mode MODE`:                 "FPF" (Frame Per Frame) for manual iteration (by pressing space) or "default" for automatic iteration.
- `--filter FILTER`:             Option for selecting a folder with filtered point cloud -> The folder should be located in the same directory as the other lidar data. Its name is defined in the script pointcloud_filter_sys or pointcloud_filter_layer and is either "data_sys_reduced_x{value}" or "data_layer_reduced_x{value}".  Default is "data" for no filtering.

### Examples
`python simulate_data.py --folder_path "\data\kitti\0051" --time_step 0.1 --mode "FPF" --filter "data_layer_reduced_x2"`
`python simulate_data.py --folder_path "\data\kitti\0051" --time_step 0.5 --filter "data_sys_reduced_x2"`
`python simulate_data.py --folder_path "\data\nuscenes\scene-0001" --time_step 0.5"`








# Examples

# Open Issues
here nuScenes issue

# Credits
- Thanks to [zhulf0804](https://github.com/zhulf0804/PointPillars) for his implementation of PointPillars.
- Thanks to []() for his nuScenes->Kitti converter. 

# Contact Information

Feel free to reach out to me:

- **Email:** [tobipaul50@gmail.com](mailto:tobipaul50@gmail.com)
- **LinkedIn:** [Tobias Paul](https://www.linkedin.com/in/tobias-paul-657513276/)
- **GitHub:** [@tp-codings](https://github.com/tp-codings)

Looking forward to connecting with you! 😊
