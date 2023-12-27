
from OpenGL.GL import *
import pygame
from src.TextController3D import TextController3D
import numpy as np
from configs.settings import min_tresh

class ConnectionRenderer:
    def __init__(self):
        self.origin = (0, 0, 0)

        self.initial_mouse_pos = None
        self.zoom_factor = 1.0
        self.dragging = False
        self.rotation_angles = (0,0,0)

        self.tracklet_coords = []

        self.textController3D = TextController3D()

    def rotate_scene(self, angle_x, angle_y, angle_z):
        glRotatef(angle_x, 1, 0, 0)
        glRotatef(angle_y, 0, 1, 0)
        glRotatef(angle_z, 0, 0, 1)

    def calculate_midpoint_0(self, rect):
        midGroundX = rect[0][0] + (rect[0][2] - rect[0][0])/2
        midGroundY = rect[1][0] + (rect[1][2] - rect[1][0])/2
        midGroundZ = rect[2][0] + (rect[2][2] - rect[2][0])/2
        halfHeight = abs(rect[2][4]- rect[2][0])/2
        coord = (midGroundX, midGroundY, midGroundZ + halfHeight)

        distance = np.linalg.norm(coord)
        return coord, round(distance, 2)
    
    def calculate_midpoint_1(self, rect):
        midX = rect[0] 
        midY = rect[1]
        midZ = rect[2] + rect[5] / 2
        coord = (midX, midY, midZ)

        distance = np.linalg.norm(coord)
        return coord, round(distance, 2)

    def render_line(self, tracklet_coord):
        glBegin(GL_LINES)
        glVertex3fv(tracklet_coord)
        glVertex3fv(self.origin)
        glEnd()

    def update(self, initial_mouse_pos, zoom_factor, dragging, mode, rects, types, scores = None):
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

        temp = []  
        # print(types)  
        if types is not None and rects is not None:
            if mode == 0:
                for rect in rects:
                    temp.append(self.calculate_midpoint_0(rect))
            elif mode == 1:
                for i, rect in enumerate(rects):
                    if scores[i] > min_tresh:
                        temp.append(self.calculate_midpoint_1(rect))
        
        self.tracklet_coords = temp

        self.textController3D.update(temp) # data


    def render(self):
        glPushMatrix()
        scale = 10
        glScalef(scale, scale, scale)
        glTranslatef(0.0, 0.0, -70 * self.zoom_factor)
        self.rotate_scene(*self.rotation_angles)
        self.textController3D.render()

        if self.tracklet_coords != None:
            for coord in self.tracklet_coords:
                self.render_line(coord[0])

        glPopMatrix()