from pygame.locals import DOUBLEBUF, OPENGL, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame

from src.PointCloudController import PointCloudController
from src.CamController import CamController
from src.InputController import InputController
from src.TextController import TextController


def init():
    global inputController, pointCloudController, camController, textController, stop, clock
    display = (800, 1000)
    stop = False
    clock = pygame.time.Clock()
    pygame.init()
    pygame.display.set_caption("KITTI Visualization")
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    gluPerspective(45, (800 / 600), 0.1, 10000.0)
    glTranslatef(0.0, 0.0, -70)
    pointCloudController = PointCloudController()
    camController = CamController()
    inputController = InputController()
    textController = TextController()

def update():
    global stop
    stop, initial_mouse_pos, zoom_factor, dragging = inputController.update()
    #camController.update(next_frame)
    pointCloudController.update(initial_mouse_pos, zoom_factor, dragging)
    fps = clock.get_fps()
    textController.update(fps, 49.0, 6.0, 300)


def render():
    clock.tick(20)  
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    #inputController.render()
    #camController.render()
    pointCloudController.render()
    textController.render()

    pygame.display.flip()



if __name__ == "__main__":
    init()
    while not stop:
        update()
        render()

    pygame.quit()