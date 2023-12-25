from OpenGL.GL import *
from configs.settings import colors, base_directory, min_tresh
from utils.utilities import incrementString
import pygame
import os
import numpy as np
import torch

from utils import read_points, keep_bbox_from_lidar_range
from model import PointPillars


class PointPillarsPredictionTest:
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

        #Modelsetup
        self.class_names = ["Pedestrian", "Cyclist", "Car"]
        self.pcd_limit_range = np.array([-50.0, -40, -3, 70.4, 40, 0.0], dtype=np.float32)
        self.ckpt = "pillar_logs/checkpoints/PP_MOF_160.pth"

        self.model = PointPillars(nclasses=len(self.class_names)).cuda()
        self.model.load_state_dict(torch.load(self.ckpt))


        #np.set_printoptions(suppress=True)


    def predict_data(self, file_path):
        pc = read_points(file_path)

        pc_torch = torch.from_numpy(pc)

        self.model.eval()
        with torch.no_grad():
            pc_torch = pc_torch.cuda()
            
            result_filter = self.model(batched_pts=[pc_torch], 
                                mode='test')[0]

        #result_filter = keep_bbox_from_lidar_range(result_filter, self.pcd_limit_range)
        lidar_bboxes = result_filter['lidar_bboxes']
        labels, scores = result_filter['labels'], result_filter['scores']
        self.tracklet_rects = lidar_bboxes
        self.tracklet_types = labels
        self.tracklet_scores = scores
        #print("PP ", self.current_frame)
        #print(lidar_bboxes)
        #print("---------------------------------------")


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
                if self.tracklet_scores[i] > min_tresh:
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
            [np.cos(yaw), np.sin(yaw), 0],
            [-np.sin(yaw), np.cos(yaw), 0],
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
