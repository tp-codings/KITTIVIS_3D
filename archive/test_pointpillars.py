import argparse
import cv2
import numpy as np
import os
import torch
import pdb

from utils import read_points, keep_bbox_from_lidar_range, vis_pc
    
from model import PointPillars

def main(args):
    CLASSES = {
        'Pedestrian': 0, 
        'Cyclist': 1, 
        'Car': 2
        }
    pcd_limit_range = np.array([-50.0, -40, -3, 70.4, 40, 0.0], dtype=np.float32)

    model = PointPillars(nclasses=len(CLASSES)).cuda()
    model.load_state_dict(torch.load(args.ckpt))

    if not os.path.exists(args.pc_path):
        raise FileNotFoundError 
    pc = read_points(args.pc_path)

    pc_torch = torch.from_numpy(pc)

    model.eval()
    with torch.no_grad():
        pc_torch = pc_torch.cuda()
        
        result_filter = model(batched_pts=[pc_torch], 
                            mode='test')[0]

    result_filter = keep_bbox_from_lidar_range(result_filter, pcd_limit_range)
    lidar_bboxes = result_filter['lidar_bboxes']
    labels, scores = result_filter['labels'], result_filter['scores']
    print(lidar_bboxes)
    
    vis_pc(pc, bboxes=lidar_bboxes, labels=labels)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Configuration Parameters')
    parser.add_argument('--ckpt', default='pillar_logs/checkpoints/epoch_160.pth', help='your checkpoint for kitti')
    parser.add_argument('--pc_path', help='your point cloud path')
    args = parser.parse_args()

    main(args)
