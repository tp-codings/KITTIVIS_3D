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
## Main visualization tool: main.py
The main.py is responsible for the interactive visualization of sensor data and the inference results of object detection. It contains the game loop, in which unnecessary components can be toggled on and off. No UI has been developed for this purpose, but it can easily be integrated into the architecture using various conditions triggered by potential buttons. This script only needs to be executed and has no additional parameters. The following image depicts the general architecture of the visualization tool following the update-render-pattern known from video games:

![architecture](https://github.com/tp-codings/KITTIVIS_3D/assets/118997294/4eaba372-c658-408b-a3c9-d2d9561b5585)


The application retrieves the data to be visualized from the directory /data/source/*. If no image is displayed, it means there are no data available in this directory. The data can be simulated using the script simulate_data.py (further described below).









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
