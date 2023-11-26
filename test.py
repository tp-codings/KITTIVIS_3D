from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import compileShader, compileProgram
import pygame
import numpy as np
from utils.settings import colors
from utils.simulateData import simulate_tracklets
from utils.utilities import incrementString

# Vertex shader source code
vertex_shader_source = """
#version 330 core
layout (location = 0) in vec3 aPos;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
void main()
{
    gl_Position = projection * view * model * vec4(aPos, 1.0);
}
"""

# Fragment shader source code
fragment_shader_source = """
#version 330 core
out vec4 FragColor;
uniform vec3 color;
void main()
{
    FragColor = vec4(color, 1.0);
}
"""

class BoundingBoxController:
    def __init__(self):
        self.current_frame = "0000000000"
        self.last_frame = ""
        self.tracklet_rects = None
        self.tracklet_types = None

        self.initial_mouse_pos = None
        self.zoom_factor = 1.0
        self.dragging = False
        self.rotation_angles = (0, 0, 0)

        self.shader_program = None
        self.VAO = None
        self.VBO = None

    def setup_shader(self):
        vertex_shader = compileShader(vertex_shader_source, GL_VERTEX_SHADER)
        fragment_shader = compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)
        self.shader_program = compileProgram(vertex_shader, fragment_shader)

    def setup_vbo(self):
        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)

        vertices = np.array([
            # Define your bounding box vertices here
        ], dtype=np.float32)

        self.VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        # Set the vertex attribute pointers
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat), ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # Unbind the VAO and VBO
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def get_tracklets(self):
        self.tracklet_rects, self.tracklet_types = simulate_tracklets()

    def rotate_scene(self, angle_x, angle_y, angle_z):
        glRotatef(angle_x, 1, 0, 0)
        glRotatef(angle_y, 0, 1, 0)
        glRotatef(angle_z, 0, 0, 1)

    def update(self, initial_mouse_pos, zoom_factor, dragging):
        self.initial_mouse_pos = initial_mouse_pos
        self.zoom_factor = zoom_factor
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

    def render(self, projection):
        glUseProgram(self.shader_program)
        glUniformMatrix4fv(glGetUniformLocation(self.shader_program, "projection"), 1, GL_FALSE, projection)

        if self.tracklet_rects is not None and self.tracklet_types is not None:
            for t_rects, t_type in zip(self.tracklet_rects, self.tracklet_types):
                self.render_3d_bounding_box(t_rects, axes=[0, 1, 2], color=colors.get(t_type, (1.0, 1.0, 1.0)))

        glUseProgram(0)

    def render_3d_bounding_box(self, vertices, axes=[0, 1, 2], color=(0, 0, 0)):
        glBindVertexArray(self.VAO)
        glLineWidth(2.0)
        scale = 10
        model = np.identity(4, dtype=np.float32)
        model = np.dot(model, np.array([
            [scale, 0, 0, 0],
            [0, scale, 0, 0],
            [0, 0, scale, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32))
        glUniformMatrix4fv(glGetUniformLocation(self.shader_program, "model"), 1, GL_FALSE, model)

        view = np.identity(4, dtype=np.float32)
        glUniformMatrix4fv(glGetUniformLocation(self.shader_program, "view"), 1, GL_FALSE, view)

        glTranslatef(0.0, 0.0, -70 * self.zoom_factor)
        self.rotate_scene(*self.rotation_angles)

        glUniform3fv(glGetUniformLocation(self.shader_program, "color"), 1, color)

        glDrawArrays(GL_LINES, 0, len(vertices) // 3)

        glBindVertexArray(0)


def main():
    pygame.init()
    pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)

    gluPerspective(45, (800 / 600), 0.1, 10000.0)
    projection = glGetFloatv(GL_PROJECTION_MATRIX)

    controller = BoundingBoxController()
    controller.setup_shader()
    controller.setup_vbo()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        controller.update(pygame.mouse.get_pos(), 1.0, False)
        controller.render(projection)

        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
