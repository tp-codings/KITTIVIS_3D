from random import randint, uniform, choice
import numpy as np

def simulate_tracklets():
    def generate_random_tracklet():
        h = uniform(1.5, 2.5)  
        w = uniform(1.0, 2.0) 
        l = uniform(1.0, 5.0)  
        rotation = uniform(0, 2 * np.pi) 
        tracklet_type = choice(['Car', 'Pedestrian'])  
        position = np.array([uniform(-50.0, 50.0), uniform(-50.0, 50.0), uniform(-1.0, 2.0)])
        return position, rotation, h, w, l, tracklet_type

    amount = randint(1, 20)
    tracklets_rect = []
    tracklets_types = []

    for _ in range(amount):
        position, rotation, h, w, l, tracklet_type = generate_random_tracklet()
        tracklet_box = np.array([
            [-l / 2, -l / 2, l / 2, l / 2, -l / 2, -l / 2, l / 2, l / 2],
            [w / 2, -w / 2, -w / 2, w / 2, w / 2, -w / 2, -w / 2, w / 2],
            [0.0, 0.0, 0.0, 0.0, h, h, h, h]
        ])

        # Rotation um die z-Achse
        rot_mat = np.array([
            [np.cos(rotation), -np.sin(rotation), 0.0],
            [np.sin(rotation), np.cos(rotation), 0.0],
            [0.0, 0.0, 1.0]
        ])

        # Transformation in die Weltkoordinaten
        tracklet_rect = np.dot(rot_mat, tracklet_box) + np.tile(position, (8, 1)).T

        tracklets_rect.append(tracklet_rect)
        tracklets_types.append(tracklet_type)

    return tracklets_rect, tracklets_types