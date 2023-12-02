import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

bboxes_3d = [
    [14.758340835571289, -1.0538733005523682, -1.5589320659637451, 3.75620436668396, 1.6059954166412354, 1.5587292909622192, -0.31324076652526855], 
    [6.437729835510254, -3.86793851852417, -1.7354700565338135, 3.1477277278900146, 1.4600247144699097, 1.4284608364105225, -0.29960644245147705], 
    [8.112299919128418, 1.2169690132141113, -1.6340510845184326, 3.666242837905884, 1.573128581047058, 1.5916444063186646, 2.816124439239502], 
    [20.169767379760742, -8.431002616882324, -1.668980360031128, 2.3815982341766357, 1.5175389051437378, 1.5693395137786865, -0.3255230188369751], 
    [33.455772399902344, -7.0356364250183105, -1.3376493453979492, 4.2138671875, 1.7446216344833374, 1.6696945428848267, 2.828645944595337], 
    [55.62187194824219, -20.328502655029297, -1.3771297931671143, 4.370806694030762, 1.7359663248062134, 1.706689715385437, 2.850411891937256], 
    [3.637751817703247, 2.738185167312622, -1.6892019510269165, 3.720982789993286, 1.5820039510726929, 1.517714023590088, -0.23044192790985107], 
    [25.040895462036133, -10.156421661376953, -1.6325522661209106, 3.7395005226135254, 1.6085299253463745, 1.4839826822280884, -0.3296833038330078], 
    [28.725183486938477, -1.552552342414856, -1.2023828029632568, 3.6942551136016846, 1.5429662466049194, 1.561034083366394, 1.241648554801941], 
    [40.870792388916016, -9.749103546142578, -1.3669278621673584, 3.8332695960998535, 1.652874231338501, 1.569952368736267, -0.28838253021240234]
]

def draw_box(x, y, z, x_size, y_size, z_size, yaw):
    vertices = np.array([
        [-x_size/2, -y_size/2, -z_size/2],
        [ x_size/2, -y_size/2, -z_size/2],
        [ x_size/2,  y_size/2, -z_size/2],
        [-x_size/2,  y_size/2, -z_size/2],
        [-x_size/2, -y_size/2,  z_size/2],
        [ x_size/2, -y_size/2,  z_size/2],
        [ x_size/2,  y_size/2,  z_size/2],
        [-x_size/2,  y_size/2,  z_size/2]
    ])
    
    rotation_matrix = np.array([
        [np.cos(yaw), -np.sin(yaw), 0],
        [np.sin(yaw), np.cos(yaw), 0],
        [0, 0, 1]
    ])

    rotated_vertices = vertices.dot(rotation_matrix.T)

    glPushMatrix()
    glTranslatef(x, y, z)

    glBegin(GL_LINES)
    for edge in [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]:
        for vertex in edge:
            glVertex3f(rotated_vertices[vertex][0], rotated_vertices[vertex][1], rotated_vertices[vertex][2])
    glEnd()

    glPopMatrix()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 500.0)
    glTranslatef(0.0, 0.0, -50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for bbox in bboxes_3d:
            draw_box(*bbox)

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
