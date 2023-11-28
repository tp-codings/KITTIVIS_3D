
from OpenGL.GL import *

class ConnectionRenderer:
    def __init__(self):
        self.tracklet_rects = None
        self.tracklet_types = None
        self.origin = (0, 0, 0)

    def render_line(self, tracklet_coord):
        glBegin(GL_LINES)
        glVertex3fv(tracklet_coord)
        glVertex3fv(self.origin)
        glEnd()

    def update(self, rects, types):
        self.tracklet_rects = rects
        self.tracklet_types = types

    def render(self):
        if self.tracklet_types != None and self.tracklet_rects  != None:
            print(self.tracklet_rects)
            for rect in self.tracklet_rects:
                self.render_line((rect[0][0], rect[1][0], rect[2][0]))