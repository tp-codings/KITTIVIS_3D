from OpenGL.GL import *
from configs.settings import colors, start_frame
from utils.utilities import incrementString
import pygame
import json
import os
import numpy as np

class BoundingBoxControllerPredictRead:
    def __init__(self):
        #hier Pfade anlegen
        self.tracklet_path = os.path.join("data", "Live", "tracklets", "data1")

        self.current_frame = start_frame
        self.last_frame = ""
        self.tracklet_rects = None
        self.tracklet_types = None

        self.initial_mouse_pos = None
        self.zoom_factor = 1.0
        self.dragging = False
        self.rotation_angles = (0,0,0)

    def parse_tracklets_data(self, file_path):
        with open(file_path, 'r') as file:
            quader_data = file.read()

        data = json.loads(quader_data)

        types_list = data["labels_3d"]
        coordinates_list = []

        for bbox_info in data["bboxes_3d"]:
            x, y, z, width, height, length, yaw = bbox_info
            coordinates_list.append([x, y, z, width, height, length, yaw])

        self.tracklet_rects = coordinates_list
        self.tracklet_types = types_list

    #def get(self):
        #return self.tracklet_rects, self.tracklet_types

    def get_tracklets(self):

        file_path = os.path.join(self.tracklet_path, self.current_frame + ".txt")
        self.parse_tracklets_data(file_path)
        next_frame = incrementString(self.current_frame)
        file_path = os.path.join(self.tracklet_path, next_frame + ".txt")
        if os.path.exists(file_path):
            self.current_frame = next_frame

              
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
        if self.tracklet_rects is not None and self.tracklet_types is not None:
            for bbox in self.tracklet_rects:
                self.render_bounding_box(*bbox)       

    def render_bounding_box(self, x, y, z, x_size, y_size, z_size, yaw):
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
