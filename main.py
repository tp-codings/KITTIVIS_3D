from pygame.locals import DOUBLEBUF, OPENGL, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame

from src.PointCloudController import PointCloudController
from src.CamController import CamController
from src.InputController import InputController
from src.TextController import TextController
from src.GeoController import GeoController
from src.BoundingBoxController import BoundingBoxController
from src.ConnectionRenderer import ConnectionRenderer

def init():
    global inputController, pointCloudController, camController, textController, geoController, boundingBoxController, connectionRenderer, stop, clock
    display = (800, 800)
    stop = False
    clock = pygame.time.Clock()
    pygame.init()
    pygame.display.set_caption("KITTI Visualization")
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    gluPerspective(45, (display[0] / display[1]), 0.1, 10000.0)
    glTranslatef(0.0, 0.0, -70)

    geoController = GeoController()
    pointCloudController = PointCloudController()
    camController = CamController(display)
    inputController = InputController()
    textController = TextController()
    boundingBoxController = BoundingBoxController()
    connectionRenderer = ConnectionRenderer()

def update():
    global stop
    stop, initial_mouse_pos, zoom_factor, dragging = inputController.update()
    camController.update()
    pointCloudController.update(initial_mouse_pos, zoom_factor, dragging)
    boundingBoxController.update(initial_mouse_pos, zoom_factor, dragging)
    latitude, longitude, height, location, speed_limit = geoController.update()
    fps = clock.get_fps()
    textController.update(fps, latitude, longitude, height, location, speed_limit)
    connectionRenderer.update(*boundingBoxController.get())


def render():
    clock.tick(30)  
    projection = glGetFloatv(GL_PROJECTION_MATRIX)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    textController.render()
    pointCloudController.render(projection)
    boundingBoxController.render()
    camController.render()
    connectionRenderer.render()
    pygame.display.flip()



if __name__ == "__main__":
    init()
    while not stop:
        update()
        render()

    pygame.quit()