import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np


class TextRenderer3D:
    def __init__(self, text="KITTI", position=(0, 0, 0), font_size=80):
        self.text = text
        self.position = position
        self.font_size = font_size
        self.font = pygame.font.SysFont('arial', font_size, bold=True)
        self.texture_id = self.render_text_as_texture()

    def render_text_as_texture(self):
        text_surface = self.font.render(self.text, True, (255, 0, 0, 255)).convert_alpha()
        original_width, original_height = text_surface.get_width(), text_surface.get_height()

        # Faktor für die Breitenvergrößerung
        width_factor = 5.0

        # Neue Breite berechnen
        new_width = int(original_width * width_factor)
        new_height = original_height  # Höhe bleibt unverändert

        # Texturdaten mit neuer Breite und Höhe generieren
        text_surface = pygame.transform.scale(text_surface, (new_width, new_height))
        text_data = pygame.image.tostring(text_surface, 'RGBA', True)

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, new_width, new_height, 0,
                    GL_RGBA, GL_UNSIGNED_BYTE, text_data)

        return texture_id

    def update(self, position, text):
        self.text = str(text) + 'm'
        self.position = tuple([x/2 for x in position])
        self.texture_id = self.render_text_as_texture()

    def render(self, camera_position = (0.0, 0.0, -70)):

        # Berechne die Rotation, um den Text zur Kamera zu richten
        glPushMatrix()
        look_at_matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
        rotation_matrix = np.array([[look_at_matrix[i][j] for j in range(4)] for i in range(4)])
        rotation_matrix_inv = np.linalg.inv(rotation_matrix[:3, :3])  # Nur die obere linke 3x3-Matrix invertieren

        # Hier wird der Vektor (0, 0, -1) von Weltkoordinaten in lokale Koordinaten transformiert
        direction_to_camera_model = np.dot(rotation_matrix_inv, [0, 0, -1])

        # Jetzt kannst du den Winkel wie zuvor berechnen
        angle = -math.atan2(direction_to_camera_model[0], direction_to_camera_model[2])
        angle_degrees = math.degrees(angle)

        glTranslatef(*self.position)
        glRotatef(angle_degrees, 0, 1, 0)

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        size = 3

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(-size, -size, 0)
        glTexCoord2f(1, 0)
        glVertex3f(size, -size, 0)
        glTexCoord2f(1, 1)
        glVertex3f(size, size, 0)
        glTexCoord2f(0, 1)
        glVertex3f(-size, size, 0)
        glEnd()

        glDisable(GL_TEXTURE_2D)
        glPopMatrix()
