from OpenGL.GL import *
from utils.settings import colors
from utils.simulateData import simulate_tracklets
from utils.utilities import incrementString
import pygame

class BoundingBoxController:
    def __init__(self):
        #hier Pfade anlegen
        self.current_frame = "0000000000"
        self.last_frame = ""
        self.tracklet_rects = None
        self.tracklet_types = None

        self.initial_mouse_pos = None
        self.zoom_factor = 1.0
        self.dragging = False
        self.rotation_angles = (0,0,0)

    def get_tracklets(self):
        self.tracklet_rects, self.tracklet_types = simulate_tracklets()   

    def rotate_scene(self, angle_x, angle_y, angle_z):
        glRotatef(angle_x, 1, 0, 0)
        glRotatef(angle_y, 0, 1, 0)
        glRotatef(angle_z, 0, 0, 1)

    def update(self, initial_mouse_pos, zoom_factor, dragging):
        self.initial_mouse_pos = initial_mouse_pos
        self.zoom_facor = zoom_factor
        self.dragging = dragging
        self.current_frame = incrementString(self.current_frame)

        if dragging:
            rel_x, rel_y = pygame.mouse.get_pos()[0] - initial_mouse_pos[0], pygame.mouse.get_pos()[1] - initial_mouse_pos[1]
            self.rotation_angles = (
                self.rotation_angles[0] + rel_y * 0.1,
                self.rotation_angles[1],
                self.rotation_angles[2] + rel_x * 0.1
            )
            print(self.rotation_angles)

        if self.last_frame != self.current_frame:
            self.get_tracklets()
            self.last_frame = self.current_frame

    def render(self):
        if self.tracklet_rects is not None and self.tracklet_types is not None:
            for t_rects, t_type in zip(self.tracklet_rects, self.tracklet_types):
                self.render_3d_bounding_box(t_rects, axes=[0, 1, 2], color=colors.get(t_type, (1.0, 1.0, 1.0)))          

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
