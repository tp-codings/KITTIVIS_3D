import os
import numpy as np
from utils.utilities import incrementString
from src.shader.pointCloudShader import vertex_shader, fragment_shader
from utils.shaderHandler import init_shader_program
from OpenGL.GL import *
import pygame


class PointCloudController:
    def __init__(self, **kwargs):
        self.velo_path = os.path.join("data", "Live", "velodyne_points", "data")
        self.current_frame = "0000000000"
        self.rotation_angles = (0,0,0)
        self.zoom_factor = 1.0
        self.vbo = self.load_point_vbo(np.array(1))
        self.velo_range = 0
        self.shader_program = init_shader_program(vertex_shader, fragment_shader)

    def get_data(self):
        file_path = os.path.join(self.velo_path, self.current_frame + ".bin")
        scan = np.fromfile(file_path, dtype=np.float32)
        next_frame = incrementString(self.current_frame)
        file_path = os.path.join(self.velo_path, next_frame + ".bin")
        if os.path.exists(file_path):
            self.current_frame = next_frame
        return scan.reshape((-1, 4))
    
    def load_point_vbo(self, vertices):
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        return vbo

    def rotate_scene(self, angle_x, angle_y, angle_z):
        glRotatef(angle_x, 1, 0, 0)
        glRotatef(angle_y, 0, 1, 0)
        glRotatef(angle_z, 0, 0, 1)

    def update(self, initial_mouse_pos, zoom_factor, dragging):
        self.zoom_factor = zoom_factor
        if dragging:
            rel_x, rel_y = pygame.mouse.get_pos()[0] - initial_mouse_pos[0], pygame.mouse.get_pos()[1] - initial_mouse_pos[1]
            self.rotation_angles = (
                self.rotation_angles[0] + rel_y * 0.1,
                self.rotation_angles[1],
                self.rotation_angles[2] + rel_x * 0.1
            )

        points_step = int(1. / 1.)
        data = self.get_data()
        self.velo_range = range(0, data.shape[0], points_step)
        self.vbo = self.load_point_vbo(data[self.velo_range, :-1])


    def render(self, projection):
        glPushMatrix()
        scale = 10
        glScalef(scale, scale, scale)
        glTranslatef(0.0, 0.0, -70 * self.zoom_factor)
        self.rotate_scene(*self.rotation_angles)

        # Berechne die Model-View-Projection-Matrix und übergebe sie an den Shader
        glUseProgram(self.shader_program)
        
        modelviewprojection_loc = glGetUniformLocation(self.shader_program, "modelviewprojection")
        modelviewprojection = glGetFloatv(GL_MODELVIEW_MATRIX)
        glUniformMatrix4fv(modelviewprojection_loc, 1, GL_FALSE, np.dot(projection, modelviewprojection))

        glPointSize(1.5)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glVertexPointer(3, GL_FLOAT, 0, None)
        glEnableClientState(GL_VERTEX_ARRAY)

        glDrawArrays(GL_POINTS, 0, len(self.velo_range))

        glDisableClientState(GL_VERTEX_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glUseProgram(0)  

        glPopMatrix()
        

        
