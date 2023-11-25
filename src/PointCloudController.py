import os
import numpy as np
from utils.utilities import incrementString
from OpenGL.GL import *
from OpenGL.GL import shaders
import pygame


class PointCloudController:
    def __init__(self, **kwargs):
        self.velo_path = os.path.join("data", "Live", "velodyne_points", "data")
        self.current_frame = "0000000000"
        self.rotation_angles = (0,0,0)
        self.zoom_factor = 1.0
        self.vbo = -1
        self.shader_program = None
        self.velo_range = 0

        self.vertex_shader = """
            #version 330
            in vec4 position;
            out float height;

            uniform mat4 modelviewprojection;

            void main()
            {
                gl_Position = modelviewprojection * position;
                height = position.z;
            }
            """
        self.fragment_shader = """
        #version 330
        in float height;
        out vec4 FragColor;

        void main()
        {
            vec3 color = mix(vec3(1.0, 1.0, 1.0), vec3(0.0, 1.0, 0.0), height);
            color = mix(color, vec3(1.0, 1.0, 0.0), height);
            color = mix(color, vec3(.0, 1.0, 0.0), height);
            
            FragColor = vec4(color, 1.0);
        }
        """

        self.init_shader_program()

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
    
    def compile_shader(self, source, shader_type):
        shader = glCreateShader(shader_type)
        glShaderSource(shader, source)
        glCompileShader(shader)

        if not glGetShaderiv(shader, GL_COMPILE_STATUS):
            raise Exception("Shader compilation failed: {}".format(glGetShaderInfoLog(shader)))

        return shader
    
    def link_program(self, vertex_shader, fragment_shader):
        program = glCreateProgram()
        glAttachShader(program, vertex_shader)
        glAttachShader(program, fragment_shader)
        glLinkProgram(program)

        if not glGetProgramiv(program, GL_LINK_STATUS):
            raise Exception("Program linking failed: {}".format(glGetProgramInfoLog(program)))

        return program
    
    def init_shader_program(self):
        vertex_shader_obj = self.compile_shader(self.vertex_shader, GL_VERTEX_SHADER)
        fragment_shader_obj = self.compile_shader(self.fragment_shader, GL_FRAGMENT_SHADER)
        self.shader_program = self.link_program(vertex_shader_obj, fragment_shader_obj)
        glDeleteShader(vertex_shader_obj)
        glDeleteShader(fragment_shader_obj)

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

    def render(self):
        glPushMatrix()
        scale = 10
        glScalef(scale, scale, scale)
        glTranslatef(0.0, 0.0, -70 * self.zoom_factor)
        self.rotate_scene(*self.rotation_angles)

        # Berechne die Model-View-Projection-Matrix und übergebe sie an den Shader
        glUseProgram(self.shader_program)
        
        modelviewprojection_loc = glGetUniformLocation(self.shader_program, "modelviewprojection")
        modelviewprojection = glGetFloatv(GL_MODELVIEW_MATRIX)
        projection = glGetFloatv(GL_PROJECTION_MATRIX)
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

        
