# KITTIVIS_3D
This is a prototype for an interactive LiDAR visualization tool for primary KITTI scene data (protoype for nuScenes data included aswell). It should also serve as the basis for the development of a live-on-board system. An 3D object detection was implemented based on the PointPillars method.

## Features
- Real time interactive data visualization for sensor data in KITTI format
- Real time 3D object detection
- Converter for nuScenes -> KITTI (only for visualization)
- Environment for training and evaluating models
  
| Personal Rating | Year of Development | Languages | Tools | Type of Application |
| --- | --- | --- | --- | --- |
| ⭐️⭐️⭐️⭐️⭐️ (5/5) | 2024 | Python | OpenGL, PyGame, CUDA, PyTorch | Visualization |

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
- `python simulate_data.py --folder_path "\data\kitti\0051" --time_step 0.1 --mode "FPF" --filter "data_layer_reduced_x2"`
- `python simulate_data.py --folder_path "\data\kitti\0051" --time_step 0.5 --filter "data_sys_reduced_x2"`
- `python simulate_data.py --folder_path "\data\nuscenes\scene-0001" --time_step 0.5"`

### Exiting the script
Once the script is terminated (with Ctrl + c), a clean-up procedure is initiated, which deletes all simulated data. However, this only occurs if the script is terminated properly. For instance, if the terminal is closed, the data will remain. However, running and terminating the script again will delete the data once more.

#  Preparing data for visualization
## Data source
KITTI raw data can be downloaded [here](https://www.cvlibs.net/datasets/kitti/raw_data.php). You have to create an account to access the files. 
You should download the "synced+rectified data" (senor data), "calibration" (sensor calibration information) and "tracklets" (annotation for ground-truth) from here.

## Extracting tracklets frame per frame: extract_per_frame_tracklets.py
The annotations of the ground-truth data are stored in a single large tracklets.xml file. These annotations need to be extracted frame by frame and tagged with the corresponding frame-specific indices. This task is handled by the script extract_per_frame_tracklets.py.

### Parameter
- `-h, --help`:               Show this help message and exit.
- `--n_frames N_FRAMES`:      Number of frames in the dataset.
- `--xml_path XML_PATH`:      Path to the tracklets XML.
- `--output_dir OUTPUT_DIR`:  Directory to save the output text files.

### Example
- `python extract_per_frame_tracklets.py --n_frames 438 --xml_path "data/0091/tracklet_labels.xml" --output_dir "data/0091/tracklets"`
  
## KITTI data format
After the extraction the folder structure should look similar to the following:
```bash
.
└── data/kitti/<scene>/
    ├── image_00/
    │   ├── [x.png]
    │   └── ...
    ├── image_01/
    │   ├── [x.png]
    │   └── ...
    ├── image_02/
    │   ├── [x.png]
    │   └── ...
    ├── image_03/
    │   ├── [x.png]
    │   └── ...
    ├── oxts/
    │   ├── [x.txt]
    │   └── ...
    ├── tracklets/
    │   ├── [x.txt]
    │   └── ...
    ├── velodyne_points/
    │   ├── [x.bin]
    │   └── ...
    └── <meta_data>.txt
```
Now you are ready to simulate!

# Filtering pointclouds
This project includes two methods for filtering point clouds. These methods allow for investigating how a model performs on reduced datasets.
The first method systematically filters the point cloud by a certain factor, simulating a generally lower data availability typical of cheaper LiDAR sensors with lower resolution.
The second method reduces based on the layers or beams of the LiDAR scanner. In this approach, every x-th layer is removed. This simulates a scanner that captures fewer layers (KITTI: 64 layers, nuScenes: 32 layers). Both scripts can be used in a similar way.

## Systematic filtering: pointcloud_filter_sys.py
This script deletes all points except every x-th point from the point cloud. It stores the folder with the filtered pointcloud in the same directory as the source folder (for easy access via simulate_data.py).

## Parameter
- `-h, --help`:                    Show this help message and exit.
- `--input_folder INPUT_FOLDER`:   Path to the input folder.
- `--step STEP`:                   Filtering level (every x-th point will be retained) -> default: 2.
- `--folder_name FOLDER_NAME`:     Name of the output folder (optional) -> default: "data_sys_reduced_{step}. If you change the folder_name, you have to reference this name in the filter-parameter from simulate_data.py.

# Examples
- `python pointcloud_filter_sys.py --input_folder "data\kitti\0051\velodyne_points\data" --step 3`
- `python pointcloud_filter_sys.py --input_folder "data\kitti\0051\velodyne_points\data" --step 2 --folder_name "my_sys_filtered_pointcloud"`

## Layer filtering: pointcloud_filter_layer.py
This script deletes every x-th layer from the point cloud. It stores the folder with the filtered pointcloud in the same directory as the source folder (for easy access via simulate_data.py).

## Parameter
- `-h, --help`:                    Show this help message and exit.
- `--input_folder INPUT_FOLDER`:   Path to the input folder.
- `--step STEP`:                   Filtering level (every x-th layer will be deleted) -> default: 2.
- `--folder_name FOLDER_NAME`:     Name of the output folder (optional) -> default: "data_sys_reduced_{step}. If you change the folder_name, you have to reference this name in the filter-parameter from simulate_data.py.

# Examples
- `python pointcloud_filter_layer.py --input_folder "data\kitti\0051\velodyne_points\data" --step 3`
- `python pointcloud_filter_layer.py --input_folder "data\kitti\0051\velodyne_points\data" --step 2 --folder_name "my_layer_filtered_pointcloud"`

# Train your own model
## Data source
The training data can be downloaded [here](https://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=3d) from the official KITTI Vision Benchmark Suite. Be sure to create an account first to access the files.
Once downloaded, the folder structure should be set up as follows:

```bash
.
└── data/kitti/
    ├── training/
    │   ├── image_02/
    │   │   ├── [x.png]
    │   │   └── ...
    │   ├── image_03/
    │   │   ├── [x.png]
    │   │   └── ...
    │   ├── velodyne_points/
    │   │   ├── [x.bin]
    │   │   └── ...
    │   ├── calib/
    │   │   ├── [x.txt]
    │   │   └── ...
    │   └── label_2/
    │       ├── [x.txt]
    │       └── ...
    └── testing/
        ├── image_02/
        │   ├── [x.png]
        │   └── ...
        ├── image_03/
        │   ├── [x.png]
        │   └── ...
        ├── velodyne_points/
        │   ├── [x.bin]
        │   └── ...
        └── calib/
            ├── [x.txt]
            └── ...
```

# Open Issues

This is just a prototype, offering plenty of room for improvements and extensions. Some possible enhancements could include: 
- 
- 

# Credits
- Thanks to [zhulf0804](https://github.com/zhulf0804/PointPillars) for his implementation of PointPillars.
- Thanks to []() for his nuScenes->Kitti converter. 

# Contact Information

Feel free to reach out to me:

- **Email:** [tobipaul50@gmail.com](mailto:tobipaul50@gmail.com)
- **LinkedIn:** [Tobias Paul](https://www.linkedin.com/in/tobias-paul-657513276/)
- **GitHub:** [@tp-codings](https://github.com/tp-codings)

Looking forward to connecting with you! 😊
