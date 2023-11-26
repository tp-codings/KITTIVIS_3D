import os
import pygame
from utils.utilities import incrementString
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class CamController:

    def __init__(self, display):
        self.cam00_path = os.path.join("data", "Live", "image_00", "data")
        self.cam01_path = os.path.join("data", "Live", "image_01", "data")
        self.cam02_path = os.path.join("data", "Live", "image_02", "data")
        self.cam03_path = os.path.join("data", "Live", "image_03", "data")

        self.current_frame = "0000000000"

        self.cams = [None, None, None, None]

        self.positions = [(-800, display[1]/2+100), (200, display[1]/2+100), (-800, display[1]/2-100), (200, display[1]/2-100)]
    
    def get_data(self):
        file_path = os.path.join(self.cam00_path, self.current_frame + ".png")
        self.cams[0] = pygame.image.load(file_path).convert()

        file_path = os.path.join(self.cam01_path, self.current_frame + ".png")
        self.cams[1] = pygame.image.load(file_path).convert()

        file_path = os.path.join(self.cam02_path, self.current_frame + ".png")
        self.cams[2]= pygame.image.load(file_path).convert()

        file_path = os.path.join(self.cam03_path, self.current_frame + ".png")
        self.cams[3] = pygame.image.load(file_path).convert()

        next_frame = incrementString(self.current_frame)
        file_path0 = os.path.join(self.cam00_path, next_frame + ".png")
        file_path1 = os.path.join(self.cam01_path, next_frame + ".png")
        file_path2 = os.path.join(self.cam02_path, next_frame + ".png")
        file_path3 = os.path.join(self.cam03_path, next_frame + ".png")
        if os.path.exists(file_path0) and os.path.exists(file_path1) and os.path.exists(file_path2) and os.path.exists(file_path3):
            self.current_frame = next_frame

    def update(self):
        self.get_data()

    def render(self, scale = 0.5, detections = None):
        for i, position in enumerate(self.positions):
            x = position[0]
            y = position[1]
            width, height = self.cams[i].get_width(), self.cams[i].get_height()
            texture_data = pygame.image.tostring(self.cams[i], "RGBA", True)

            glEnable(GL_TEXTURE_2D)
            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

            tl = (x/20, y/20)
            tr = (x/20 + width*scale/20, y/20)

            br = (x/20 + width*scale/20, y/20 - height*scale/20)
            bl = (x/20, y/20 - height*scale/20)

            glBegin(GL_QUADS)
            glTexCoord2f(0, 1)
            glVertex2f(tl[0], tl[1])  # Oben links
            glTexCoord2f(1, 1)
            glVertex2f(tr[0], tr[1])  # Oben rechts
            glTexCoord2f(1, 0)
            glVertex2f(br[0], br[1])  # Unten rechts
            glTexCoord2f(0, 0)
            glVertex2f(bl[0], bl[1])  # Unten links
            glEnd()

            glDeleteTextures([texture_id])
            glDisable(GL_TEXTURE_2D)