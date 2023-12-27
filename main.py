from pygame.locals import DOUBLEBUF, OPENGL, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from OpenGL.GL import *
from OpenGL.GLU import *
#from OpenGL.GLUT import *
import pygame

from src.PointCloudController import PointCloudController
from src.CamController import CamController
from src.InputController import InputController
from src.TextController import TextController
from src.GeoController import GeoController
from src.BoundingBoxControllerGroundTruth import BoundingBoxControllerGroundTruth
from src.BoundingBoxControllerPredictRead import BoundingBoxControllerPredictRead
from src.PointPillarsPredictionTest import PointPillarsPredictionTest
from src.BoundingBoxControllerPredict import BoundingBoxControllerPredict
from src.ConnectionRenderer import ConnectionRenderer
import numpy as np

def init():
    global inputController, pointCloudController, camController, textController, geoController, boundingBoxControllerGroundTruth, boundingBoxControllerPredict, pointPillarsPredictionTest, connectionRenderer, stop, clock
    display = (800, 800)
    stop = False
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption("KITTI Visualization")
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    gluPerspective(45, (display[0] / display[1]), 0.1, 100000.0)
    glTranslatef(0.0, 0.0, -70)

    geoController = GeoController()
    pointCloudController = PointCloudController()
    camController = CamController(display)
    inputController = InputController()
    textController = TextController()

    boundingBoxControllerGroundTruth = BoundingBoxControllerGroundTruth()

    boundingBoxControllerPredict = BoundingBoxControllerPredict()

    pointPillarsPredictionTest = PointPillarsPredictionTest()

    connectionRenderer = ConnectionRenderer()



def update():
    global stop
    stop, initial_mouse_pos, zoom_factor, dragging = inputController.update()
    #camController.update()
    pointCloudController.update(initial_mouse_pos, zoom_factor, dragging)

    #boundingBoxControllerGroundTruth.update(initial_mouse_pos, zoom_factor, dragging)

    #boundingBoxControllerPredict.update(initial_mouse_pos, zoom_factor, dragging)

    pointPillarsPredictionTest.update(initial_mouse_pos, zoom_factor, dragging)

    latitude, longitude, height = geoController.update()
    fps = clock.get_fps()
    textController.update(str(round(fps, 2)), str(round(latitude, 6)), str(round(longitude, 6)), str(round(height, 2)), str(pointCloudController.get_point_count()))

    #connectionRenderer.update(initial_mouse_pos, zoom_factor, dragging, 0, *boundingBoxControllerGroundTruth.get())
    #connectionRenderer.update(initial_mouse_pos, zoom_factor, dragging, 1, *boundingBoxControllerPredict.get())
    connectionRenderer.update(initial_mouse_pos, zoom_factor, dragging, 1, *pointPillarsPredictionTest.get())



def render():
    clock.tick(60)  
    projection = glGetFloatv(GL_PROJECTION_MATRIX)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    pointCloudController.render(projection)
    textController.render()
    #boundingBoxControllerGroundTruth.render()

    #boundingBoxControllerPredict.render()

    pointPillarsPredictionTest.render()

    #camController.render()
    connectionRenderer.render()
    pygame.display.flip()

if __name__ == "__main__":
    init()
    while not stop:
        update()
        render()
    pygame.quit()