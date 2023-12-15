from mmdet3d.apis import init_model, inference_detector
from OpenGL.GL import *
from configs.settings import colors, base_directory
from utils.utilities import incrementString
import pygame
import json
import os
import numpy as np

class BoundingBoxControllerPredict:
    def __init__(self):
        #hier Pfade anlegen
        self.velo_path = os.path.join(base_directory, "velodyne_points", "source")

        self.current_frame = "0000000000"
        self.last_frame = ""
        self.tracklet_rects = None
        self.tracklet_types = None
        self.tracklet_scores = None

        self.initial_mouse_pos = None
        self.zoom_factor = 1.0
        self.dragging = False
        self.rotation_angles = (0,0,0)

        self.config_file = 'configs/pointpillars_hv_secfpn_8xb6-160e_kitti-3d-3class.py'
        self.checkpoint_file = 'weights/hv_pointpillars_secfpn_6x8_160e_kitti-3d-3class_20220301_150306-37dc2420.pth'
        self.model = init_model(self.config_file, self.checkpoint_file, device="cuda:0")

        self.class_names = ["Pedestrian", "Cyclist", "Car"]
        np.set_printoptions(suppress=True)



    def predict_data(self, file_path):
        results, _ = inference_detector(self.model, file_path)

        bboxes_3d = results.pred_instances_3d.get("bboxes_3d").tensor.cpu().numpy()
        labels_3d = results.pred_instances_3d.get("labels_3d").cpu().numpy()
        scores_3d = results.pred_instances_3d.get("scores_3d").cpu().numpy()
        
        print("OpenDet")
        print(bboxes_3d)
        # print(labels_3d)
        # print(scores_3d)

        self.tracklet_rects = bboxes_3d
        self.tracklet_types = labels_3d
        self.tracklet_scores = scores_3d

    def get(self):
        return self.tracklet_rects, self.tracklet_types, self.tracklet_scores

    def get_tracklets(self):

        file_path = os.path.join(self.velo_path, self.current_frame + ".bin")
        if os.path.exists(file_path):
            self.predict_data(file_path)

            next_frame = incrementString(self.current_frame)
            file_path = os.path.join(self.velo_path, next_frame + ".bin")
            if os.path.exists(file_path):
                #print(self.tracklet_rects)

                self.current_frame = next_frame
        else:
            print(f"no data for tracklet prediction at: {file_path}")
            self.tracklet_rects = None
            self.tracklet_types = None
            self.tracklet_scores = None
            self.current_frame = "0000000000"


              
    def rotate_scene(self, angle_x, angle_y, angle_z):
        glRotatef(angle_x, 1, 0, 0)
        glRotatef(angle_y, 0, 1, 0)
        glRotatef(angle_z, 0, 0, 1)

    def update(self, initial_mouse_pos, zoom_factor, dragging):
        self.initial_mouse_pos = initial_mouse_pos
        self.zoom_factor = zoom_factor
        self.dragging = dragging
        
        if dragging:
            rel_x, rel_y = pygame.mouse.get_pos()[0] - initial_mouse_pos[0], pygame.mouse.get_pos()[1] - initial_mouse_pos[1]
            self.rotation_angles = (
                self.rotation_angles[0] + rel_y * 0.1,
                self.rotation_angles[1],
                self.rotation_angles[2] + rel_x * 0.1
            )

        self.get_tracklets()

    def render(self):
        if self.tracklet_rects is not None and self.tracklet_types is not None and self.tracklet_scores is not None:
            for i, bbox in enumerate(self.tracklet_rects):
                if self.tracklet_scores[i] > 0.5:
                    self.render_bounding_box(*bbox, i)       

    def render_bounding_box(self, x, y, z, x_size, y_size, z_size, yaw, index):
        vertices = np.array([
            [-x_size/2, -y_size/2, 0],
            [ x_size/2, -y_size/2, 0],
            [ x_size/2,  y_size/2, 0],
            [-x_size/2,  y_size/2, 0],
            [-x_size/2, -y_size/2,  z_size],
            [ x_size/2, -y_size/2,  z_size],
            [ x_size/2,  y_size/2,  z_size],
            [-x_size/2,  y_size/2,  z_size]
        ])
        
        rotation_matrix = np.array([
            [np.cos(yaw), -np.sin(yaw), 0],
            [np.sin(yaw), np.cos(yaw), 0],
            [0, 0, 1]
        ])

        rotated_vertices = vertices.dot(rotation_matrix.T)

        glPushMatrix()
        scale = 10
        glScalef(scale, scale, scale)
        glTranslatef(0.0, 0.0, -70 * self.zoom_factor)
        self.rotate_scene(*self.rotation_angles)
        glPushAttrib(GL_CURRENT_BIT)
        glTranslatef(x, y, z)
        glColor3fv(colors[self.class_names[self.tracklet_types[index]].lower()])
        #glColor3fv((1,1,1))
        glBegin(GL_LINES)
        for edge in [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]:
            for vertex in edge:
                glVertex3f(rotated_vertices[vertex][0], rotated_vertices[vertex][1], rotated_vertices[vertex][2])
        glEnd()
        glPopAttrib()
        glPopMatrix()
