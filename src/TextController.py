from pygame import font, image
from OpenGL.GL import *

class TextController:
    def __init__(self):
        self.font = font.SysFont('arial', 20)
        self.fps = 0
        self.latitude = 0
        self.longitude = 0
        self.height = 0

    def render_text(self, x, y, text):                                                
        position = (x, y, 0)
        textSurface = self.font.render(text, True, (255, 255, 66, 255)).convert_alpha()
        textData = image.tostring(textSurface, "RGBA", True)
        glRasterPos3d(*position)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

    def update(self, fps, latitude, longitude, height):
        self.fps = fps
        self.latitude = latitude
        self.longitude = longitude
        self.height = height

    def render(self):
        self.render_text(-35, 25, str(round(self.fps, 2)))
        self.render_text(-35, 23, "Latitude: " + str(round(self.latitude, 6)))
        self.render_text(-35, 21, "Longitude: " + str(round(self.longitude, 6)))
        self.render_text(-35, 19, "Height: " + str(round(self.height, 2)))