import os
import numpy as np
import argparse
from utils import parseTrackletXML as xmlParser

def load_tracklets_for_frames(n_frames, xml_path, output_dir):
    """
    Loads dataset labels also referred to as tracklets, saving them individually for each frame.

    Parameters
    ----------
    n_frames    : Number of frames in the dataset.
    xml_path    : Path to the tracklets XML.
    output_dir  : Directory to save the output text files.

    Returns
    -------
    None
    """
    tracklets = xmlParser.parseXML(xml_path)

    frame_tracklets = {}
    frame_tracklets_types = {}
    for i in range(n_frames):
        frame_tracklets[i] = []
        frame_tracklets_types[i] = []

    # loop over tracklets
    for i, tracklet in enumerate(tracklets):
        # this part is inspired by kitti object development kit matlab code: computeBox3D
        h, w, l = tracklet.size
        # in velodyne coordinates around zero point and without orientation yet
        trackletBox = np.array([
            [-l / 2, -l / 2, l / 2, l / 2, -l / 2, -l / 2, l / 2, l / 2],
            [w / 2, -w / 2, -w / 2, w / 2, w / 2, -w / 2, -w / 2, w / 2],
            [0.0, 0.0, 0.0, 0.0, h, h, h, h]
        ])
        # loop over all data in tracklet
        for translation, rotation, state, occlusion, truncation, amtOcclusion, amtBorders, absoluteFrameNumber in tracklet:
            # determine if object is in the image; otherwise continue
            if truncation not in (xmlParser.TRUNC_IN_IMAGE, xmlParser.TRUNC_TRUNCATED):
                continue
            # re-create 3D bounding box in velodyne coordinate system
            yaw = rotation[2]  # other rotations are supposedly 0
            assert np.abs(rotation[:2]).sum() == 0, 'object rotations other than yaw given!'
            rotMat = np.array([
                [np.cos(yaw), -np.sin(yaw), 0.0],
                [np.sin(yaw), np.cos(yaw), 0.0],
                [0.0, 0.0, 1.0]
            ])
            cornerPosInVelo = np.dot(rotMat, trackletBox) + np.tile(translation, (8, 1)).T
            frame_tracklets[absoluteFrameNumber] = frame_tracklets[absoluteFrameNumber] + [cornerPosInVelo]
            frame_tracklets_types[absoluteFrameNumber] = frame_tracklets_types[absoluteFrameNumber] + [tracklet.objectType]

    # Save data to text file

    for i in range(n_frames):
        frame_output_dir = os.path.join(output_dir, f"{i:010d}.txt")
        
        with open(frame_output_dir, 'w') as file:
            for corners, obj_type in zip(frame_tracklets[i], frame_tracklets_types[i]):
                file.write(f"{obj_type} {' '.join(map(str, corners.flatten()))}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Load tracklets for frames and save them individually.')
    parser.add_argument('--n_frames', type=int, help='Number of frames in the dataset')
    parser.add_argument('--xml_path', type=str, help='Path to the tracklets XML')
    parser.add_argument('--output_dir', type=str, help='Directory to save the output text files')

    args = parser.parse_args()

    load_tracklets_for_frames(args.n_frames, args.xml_path, args.output_dir)
