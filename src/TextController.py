from pygame import font, image
from OpenGL.GL import *

class TextController:
    def __init__(self):
        self.font = font.SysFont('arial', 20)
        self.fps = 0
        self.latitude = 0
        self.longitude = 0
        self.height = 0
        self.point_count = 0

    def render_text(self, x, y, text):                                                
        position = (x, y, 0)
        textSurface = self.font.render(text, True, (0, 255, 66, 0)).convert_alpha()
        textData = image.tostring(textSurface, "RGBA", True)
        glRasterPos3d(*position)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

    def update(self, fps, latitude, longitude, height, point_count):
        self.fps = fps
        self.latitude = latitude
        self.longitude = longitude
        self.height = height
        self.point_count = point_count

    def render(self):
        self.render_text(-27, 25, self.fps)
        self.render_text(-27, 23, "Latitude: " + self.latitude)
        self.render_text(-27, 21, "Longitude: " + self.longitude)
        self.render_text(-27, 19, "Height: " + self.height)
        self.render_text(-27, 17, "Punkte: " + self.point_count)
