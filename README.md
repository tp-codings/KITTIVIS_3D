# KITTIVIS_3D: Visualization of LiDAR-Based 3D-Object detection with PointPillars
This is a prototype for an interactive LiDAR visualization tool for primary KITTI scene data (protoype for nuScenes data included aswell). It should also serve as the basis for the development of a live-on-board system. An 3D object detection was implemented based on the PointPillars method.

## Features
- Real time interactive data visualization for sensor data in KITTI format
- Real time 3D object detection
- Converter for nuScenes -> KITTI (only for visualization)
- Environment for training and evaluating models

## Project Overview
| Personal Rating | Year of Development | Languages | Tools | Type of Application |
| --- | --- | --- | --- | --- |
| ⭐️⭐️⭐️⭐️⭐️ (5/5) | 2024 | Python | OpenGL, PyGame, CUDA, PyTorch | Visualization |

# Getting Started 
## Prerequisites
- Python Version: 3.8
- Cuda Version: 12.1
- CuDNN Version: 12.x
- PyTorch Version: 2.1.1

## Hardware used:
- GPU: 1x NVIDIA RTX4070
- CPU: 1x Intel Core i5-13600KF
- RAM: 16GB

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

### Parameters
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

#  Preparing kitti data for visualization
## Data source
KITTI raw data can be downloaded [here](https://www.cvlibs.net/datasets/kitti/raw_data.php). You have to create an account to access the files. 
You should download the "synced+rectified data" (senor data), "calibration" (sensor calibration information) and "tracklets" (annotation for ground-truth) from here.

## Extracting tracklets frame per frame: extract_per_frame_tracklets.py
The annotations of the ground-truth data are stored in a single large tracklets.xml file. These annotations need to be extracted frame by frame and tagged with the corresponding frame-specific indices. This task is handled by the script extract_per_frame_tracklets.py.

### Parameters
- `-h, --help`:               Show this help message and exit.
- `--n_frames N_FRAMES`:      Number of frames in the dataset.
- `--xml_path XML_PATH`:      Path to the tracklets XML.
- `--output_dir OUTPUT_DIR`:  Directory to save the output text files.

### Example
- `python extract_per_frame_tracklets.py --n_frames 438 --xml_path "data/0091/tracklet_labels.xml" --output_dir "data/0091/tracklets"`
  
### KITTI data format
After the extraction the folder structure should look similar to the following:
```bash
.
└── data/kitti/<scene>/
    ├── image_00/data/
    │   ├── [x.png]
    │   └── ...
    ├── image_01/data/
    │   ├── [x.png]
    │   └── ...
    ├── image_02/data/
    │   ├── [x.png]
    │   └── ...
    ├── image_03/data/
    │   ├── [x.png]
    │   └── ...
    ├── oxts/data/
    │   ├── [x.txt]
    │   └── ...
    ├── tracklets/data/
    │   ├── [x.txt]
    │   └── ...
    ├── velodyne_points/<data/data_reduced>/
    │   ├── [x.bin]
    │   └── ...
    └── <meta_data>.txt
```
Now you are ready to simulate!

## Examples
<img src="https://github.com/tp-codings/KITTIVIS_3D/assets/118997294/3569caf6-600a-4f65-80fe-3c01fb8c5d47" alt="pc_vis1" width="200" height="200">

<img src="https://github.com/tp-codings/KITTIVIS_3D/assets/118997294/b56febc4-e161-4bb5-a341-25c6c07d4f1e" alt="gt_comp_mof" width="200" height="200">

<img src="https://github.com/tp-codings/KITTIVIS_3D/assets/118997294/fec8df81-9de1-49e3-a412-872863b5827b" alt="distances" width="200" height="200">

<img src="https://github.com/tp-codings/KITTIVIS_3D/assets/118997294/c7cb5e7f-72ae-4a9e-8493-4c4808d559e1" alt="mof_psf" width="200" height="200">

<img src="https://github.com/tp-codings/KITTIVIS_3D/assets/118997294/c8700dd5-6e82-4e7b-a0d0-3e830127613c" alt="no_reduced_passant" width="100" height="200">

# Filtering pointclouds
This project includes two methods for filtering point clouds. These methods allow for investigating how a model performs on reduced datasets.
The first method systematically filters the point cloud by a certain factor, simulating a generally lower data availability typical of cheaper LiDAR sensors with lower resolution.
The second method reduces based on the layers or beams of the LiDAR scanner. In this approach, every x-th layer is removed. This simulates a scanner that captures fewer layers (KITTI: 64 layers, nuScenes: 32 layers). Both scripts can be used in a similar way.

## Systematic filtering: pointcloud_filter_sys.py
This script deletes all points except every x-th point from the point cloud. It stores the folder with the filtered pointcloud in the same directory as the source folder (for easy access via simulate_data.py).

### Parameters
- `-h, --help`:                    Show this help message and exit.
- `--input_folder INPUT_FOLDER`:   Path to the input folder.
- `--step STEP`:                   Filtering level (every x-th point will be retained) -> default: 2.
- `--folder_name FOLDER_NAME`:     Name of the output folder (optional) -> default: "data_sys_reduced_{step}. If you change the folder_name, you have to reference this name in the filter-parameter from simulate_data.py.

### Examples
- `python pointcloud_filter_sys.py --input_folder "data\kitti\0051\velodyne_points\data" --step 3`
- `python pointcloud_filter_sys.py --input_folder "data\kitti\0051\velodyne_points\data" --step 2 --folder_name "my_sys_filtered_pointcloud"`
  
![sys_reduced_passant](https://github.com/tp-codings/KITTIVIS_3D/assets/118997294/90149e14-0705-43d9-a499-69fa6812c231)

## Layer filtering: pointcloud_filter_layer.py
This script deletes every x-th layer from the point cloud. It stores the folder with the filtered pointcloud in the same directory as the source folder (for easy access via simulate_data.py).

### Parameters
- `-h, --help`:                    Show this help message and exit.
- `--input_folder INPUT_FOLDER`:   Path to the input folder.
- `--step STEP`:                   Filtering level (every x-th layer will be deleted) -> default: 2.
- `--folder_name FOLDER_NAME`:     Name of the output folder (optional) -> default: "data_sys_reduced_{step}. If you change the folder_name, you have to reference this name in the filter-parameter from simulate_data.py.

### Examples
- `python pointcloud_filter_layer.py --input_folder "data\kitti\0051\velodyne_points\data" --step 3`
- `python pointcloud_filter_layer.py --input_folder "data\kitti\0051\velodyne_points\data" --step 2 --folder_name "my_layer_filtered_pointcloud"`
  
![layer_reduced_passant](https://github.com/tp-codings/KITTIVIS_3D/assets/118997294/1b782369-074b-43b0-a3fd-b350cd9ddc3f)

# Train your own model
## Data source
The training data can be downloaded [here](https://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=3d) from the official KITTI Vision Benchmark Suite. Be sure to create an account first to access the files. 
If you like to train on a filtered dataset, eel free to apply the corresponding script to the point cloud folders for training and testing.
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

## Preparing kitti data for training: pre_process_kitti.py
**Note:** The following scripts are from [zhulf0804](https://github.com/zhulf0804/PointPillars) who has implemented the PointPillars method in python with PyTorch. He used a different Numpy version than I did which might lead to issues. 
To resolve this, you can either adjust the Numpy version and make the necessary modifications in the code, or create a new Conda environment based on the PointPillars implementation being used (recommended), which includes the appropriate dependencies for training.
The script pre_process_kitti.py is responsible for creating an annotation database, which is used for comparison in the training process and for the creation of Train-Val-split. On my machine it takes about 5 minutes to preprocess the dataset. After this, the folder structure should look like:

```bash
.
└── data/kitti/
    ├── kitti_gt_database/
    │   ├── <frame>_<class>_<count>.bin
    │   └── ...
    ├── training/
    ├── testing/
    ├── kitti_dbinfos_train.pkl
    ├── kitti_infos_test.pkl
    ├── kitti_infos_train.pkl
    ├── kitti_infos_trainval.pkl
    └── kitti_infos_val.pkl
```

### Parameters
- `-h, --help`:             Show this help message and exit.
- `--data_root DATA_ROOT`:  Your data root for KITTI.
- `--prefix PREFIX`:        The prefix name for the saved .pkl file.

### Examples
- `python pre_process_kitti.py --data_root {absolute path to dataset root location}`

## Train a model: train.py
**Note:** This script can be executed within the original environment.
If you want to train a model on a dataset, then the script train.py comes into play. It handles the entire training process, generates the checkpoint file, and plots the results. The progress is displayed in the terminal using tqdm. It supports TensorBoard aswell.
It is strongly recommended to use CUDA in order not to wait for centuries. On my machine it takes about 10h to train a model with 160 epochs. 

### Parameters
- `-h, --help`:                          Show this help message and exit.
- `--data_root DATA_ROOT`:               Your data root for KITTI.
- `--saved_path SAVED_PATH`:             Path to save the output -> default: "pillar_logs".
- `--batch_size BATCH_SIZE`:             Batch size for training -> default: 6.
- `--num_workers NUM_WORKERS`:           Number of workers for data loading -> default: 4.
- `--nclasses NCLASSES`:                 Number of classes -> default: 3.
- `--init_lr INIT_LR`:                   Initial learning rate -> default: 0.00025.
- `--max_epoch MAX_EPOCH`:               Maximum number of epochs for training -> default: 160.
- `--log_freq LOG_FREQ`:                 Logging frequency -> default: 8.
- `--ckpt_freq_epoch CKPT_FREQ_EPOCH`:   Checkpoint saving frequency (in epochs) -> default: 20.
- `--no_cuda`:                           Whether to use cuda.

### Examples
- `python train.py --data_root {absolute path to dataset root location}`
- `python train.py --data_root {absolute path to dataset root location} --max_epoch=300`

## Evaluate a model (KITTI Benchmark): evaluate.py
This script handles the evaluation of a trained model on a specific dataset. As output, it generates the scores in the individual categories of the KITTI benchmark. It also calculates the average inference time in ms. 
It is strongly recommended to use CUDA in order not to wait for ages. On my machine it takes about 3 minutes to evaluate a model. 

### Parameters
- `-h, --help`:                 Show this help message and exit.
- `--data_root DATA_ROOT`:      Your data root for KITTI.
- `--ckpt CKPT`:                Your checkpoint for KITTI.
- `--saved_path SAVED_PATH`:    Your saved path for predicted results.
- `--batch_size BATCH_SIZE`:    Batch size for processing -> default: 1.
- `--num_workers NUM_WORKERS`:  Number of workers for data loading -> default: 4.
- `--nclasses NCLASSES`:        Number of classes -> default: 3.
- `--no_cuda`:                  Whether to use cuda.

### Examples
- `python evaluate.py --ckpt {absolute path to checkpoint root location} --data_root {absolute path to dataset root location}`

# KITTIVIS_3D with nuScenes:
In general, the tools are completely agnostic about the data source. Essentially, it is only relevant that the data is in the correct KITTI format at the time of processing. 
For using KITTI scenes, the steps and instructions described above can be followed. If you want to use a different dataset like nuScenes or Waymo, it needs to be converted first. In this tool suite, a prototype procedure for using the nuScenes dataset is implemented. The following sections explain what can be done, how it's done, what cannot be done, and what problems still exist. Short form: Visualization and object detection in visualization tool works (no GT-Data), training and evaluating a model does not work.

## Preparing nuScenes data for visualization: nuscenes_kitti_converter.py
This script ([based on this](https://gist.github.com/jbehley/1f2a68cba1b1914bb8b23f2de08fc233)) extracts all scenes from the entire referenced dataset split and converts the associated data scene by scene into the KITTI format. It only supports the conversion of camera images and LiDAR data. The script cannot convert the ground-truth data, which is why they cannot be visualized. It has been modified to also format the LiDAR data. nuScenes LiDAR data contains a ring index, which is not provided for in the KITTI format and thus needs to be removed. The folder structure looks as follows:

```bash
.
└── data/nuscenes/scene-<scene_number>/
    ├── image_2/data/
    │   ├── [x.png]
    │   └── ...
    ├── velodyne_points/data/
    │   ├── [x.bin]
    │   └── ...
    ├── calib.txt
    ├── original.txt
    ├── original_images_2.txt
    └── poses.txt
```
### Parameters
This script does not use argparser. The usage works as follows: 
- `python nuscenes_kitti_converter.py <dataset_folder> <output_folder> [<scene_name>]`

### Examples
- `python nuscenes_kitti_converter.py {absolute path to nuscenes dataset split} "data/nuscenes"`
  
![mof_nuscenes](https://github.com/tp-codings/KITTIVIS_3D/assets/118997294/a2a569eb-aca9-44bc-9aa2-24aeb6eb311a)

## Approach for preparing nuScenes data for training and evaluating
### 1. Convert dataset: test_anns_converter.py
For training and evaluating a model, the ground-truth data is relevant. The nuscenes-dev-kit provides a conversion script that claims to convert nuScenes data into the KITTI format. Unlike the previously described script, this one does not proceed scene by scene but converts the dataset into the training-testing structure of KITTI. Usage as follows:
`python test_anns_converter.py nuscenes_gt_to_kitti <--params>`

#### Parameters
- <function>                           Function that should be uesed -> nuscenes_gt_to_kitti (for this purpose here).
- `-h, --help`:                        Show this help message and exit.
- `--nusc_kitti_dir=NUSC_KITTI_DIR`:   Path to the NuScenes-KITTI dataset directory.
- `-c, --cam_name=CAM_NAME`:           Camera name -> default: 'CAM_FRONT'.
- `-l, --lidar_name=LIDAR_NAME`:       LiDAR sensor name -> default: 'LIDAR_TOP'.
- `-i, --image_count=IMAGE_COUNT`:     Number of images to process -> default: 10.
- `--nusc_version=NUSC_VERSION`:       Version of the NuScenes dataset -> default: 'v1.0-test'.
- `-s, --split=SPLIT`:                 Data split (e.g., 'test', 'val') -> default: 'test'.
- `-d, --dataroot=DATAROOT`:           Path to the root directory of the data.

#### Examples
- `python test_anns_converter.py nuscenes_gt_to_kitti -d {absolute path to dataset root path} --nusc_kitti_dir {absolute path to desired target path}`

### 2. Convert token to index: token_to_index.py
The script test_anns_converter.py does not index the files correctly but names them with their token. The script token_to_index.py converts all filenames in the hardcoded directory to their associated indices. The following scripts are all prototypes for testing and therefore only offer very limited functionality just for testing. This script has to be applied to all folders inside both the training and the testing folder.

### 3. Convert nuScenes Ground-Truth format to KTTTI format: convert_ns_gt_to_kitti_gt.py
The converter script also does not convert the ground truth data properly. It includes classes, that are supported by nuScenes but not by KITTI. The script convert_ns_gt_to_kitti_gt.py is responsible for the conversion to the KITTI format by deleting all not supported classes. The path to the "label_2"-folder is also hardcoded. 

### 4. Remove last entry: remove_last_entry.py
For whatever reason there is an additional entry inside the GT-data, which has to be removed. For sure, you could do this inside convert_ns_gt_to_kitti_gt.py but I did not because of testing purposes. This script uses the same hardcoded path.

### Conclusion
At this point, the dataset appears to be correctly converted into the KITTI format. All files are referenced by indices, the ground-truth data corresponds to the KITTI format, the ring indizes from the LiDAR-data are removed and the folder structure also matches.
The procedure now follows the same as the one for KITTI-data because once converted to the KITTI format, the original origin of the data should not matter, as it can no longer be resolved. 
The preprocessing of the data works just fine. However, during evaluation on this dataset, index errors are being thrown, the origin of which I have not been able to identify:
![Untitled](https://github.com/tp-codings/KITTIVIS_3D/assets/118997294/db60040f-5c17-4f8c-8a78-0c90ddd3a818)
It was also peculiar that this error occurred at different points in the evaluation process and that some data passed through without a problem. Maybe someone smarter than me is able to solve this issue.

# Open Issues
This is just a prototype, offering plenty of room for improvements and extensions. Some possible enhancements could include: 
- Another system for assignment control and synchronization of individual frames as indices, onsidering the lack of guaranteed synchronization of an on-board system.
- Interactive UI for toggling components.
- Better design
- Expansion of supported classes (trams, buses, scooters, ...)
- Solution to the problem of evaluation and training on the nuScenes dataset.
- Combining preprocessing and training with parameters.
- Proper conversion of nuScenes Ground-Truth data for visualization
- many, many, many more :)

# Credits
- Thanks to [zhulf0804](https://github.com/zhulf0804/PointPillars) for his implementation of PointPillars.
- Thanks to [jbehley](https://gist.github.com/jbehley/1f2a68cba1b1914bb8b23f2de08fc233) for his nuScenes -> Kitti converter.

# Citation
``` citation1
@INPROCEEDINGS{Geiger2012CVPR,
  author = {Andreas Geiger and Philip Lenz and Raquel Urtasun},
  title = {Are we ready for Autonomous Driving? The KITTI Vision Benchmark Suite},
  booktitle = {Conference on Computer Vision and Pattern Recognition (CVPR)},
  year = {2012}
}
```
```citation2
@ARTICLE{Geiger2013IJRR,
  author = {Andreas Geiger and Philip Lenz and Christoph Stiller and Raquel Urtasun},
  title = {Vision meets Robotics: The KITTI Dataset},
  journal = {International Journal of Robotics Research (IJRR)},
  year = {2013}
}
```

# Contact Information

Feel free to reach out to me:

- **Email:** [tobipaul50@gmail.com](mailto:tobipaul50@gmail.com)
- **LinkedIn:** [Tobias Paul](https://www.linkedin.com/in/tobias-paul-657513276/)
- **GitHub:** [@tp-codings](https://github.com/tp-codings)

Looking forward to connecting with you! 😊
