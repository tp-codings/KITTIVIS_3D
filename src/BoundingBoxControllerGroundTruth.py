from OpenGL.GL import *
from configs.settings import colors
from utils.simulateData import simulate_tracklets
from utils.utilities import incrementString
import pygame
import os
import numpy as np

class BoundingBoxControllerGroundTruth:
    def __init__(self):
        #hier Pfade anlegen
        self.tracklet_path = os.path.join("data", "Live", "tracklets", "data")

        self.current_frame = "0000000000"
        self.last_frame = ""
        self.tracklet_rects = None
        self.tracklet_types = None

        self.initial_mouse_pos = None
        self.zoom_factor = 1.0
        self.dragging = False
        self.rotation_angles = (0,0,0)

    def parse_tracklets_data(self, file_path):
        with open(file_path, 'r') as file:
            quader_data = file.readlines()

        types_list = []
        coordinates_list = []

        for line in quader_data:
            data = line.split()
            if len(data) < 24:
                continue  # Skip lines with incomplete data

            quader_type = data[0]

            types_list.append(quader_type)
            coordinates_list.append(np.array([
                [float(x) for x in data[1:9]],
                [float(x) for x in data[9:17]],
                [float(x) for x in data[17:25]]
            ]))
        self.tracklet_rects = coordinates_list
        self.tracklet_types = types_list

    def get(self):
        return self.tracklet_rects, self.tracklet_types

    def get_tracklets(self):
        #self.tracklet_rects, self.tracklet_types = simulate_tracklets()  

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
            for t_rects, t_type in zip(self.tracklet_rects, self.tracklet_types):
                self.render_3d_bounding_box(t_rects, axes=[0, 1, 2], color=colors.get(t_type.lower(), (1.0, 1.0, 1.0)))          

    def render_3d_bounding_box(self, vertices, axes=[0, 1, 2], color=(0, 0, 0)):
        vertices = vertices[axes, :]
        connections = [
            [0, 1], [1, 2], [2, 3], [3, 0],
            [4, 5], [5, 6], [6, 7], [7, 4],
            [0, 4], [1, 5], [2, 6], [3, 7]
        ]
        glLineWidth(2.0)
        glPushMatrix()
        scale = 10
        glScalef(scale, scale, scale)
        glTranslatef(0.0, 0.0, -70 * self.zoom_factor)
        self.rotate_scene(*self.rotation_angles)
        glPushAttrib(GL_CURRENT_BIT)

        for connection in connections:
            glBegin(GL_LINES)
            glColor3fv(color)
            for vertex in connection:
                glVertex3fv(vertices[:, vertex])
            glEnd()
        glPopAttrib()
        glPopMatrix()
