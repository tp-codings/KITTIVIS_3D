import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Funktion zum Laden einer OBJ-Datei
def load_obj(filename):
    vertices = []
    faces = []
    
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) > 0:
                if parts[0] == 'v':
                    vertices.append(list(map(float, parts[1:])))
                elif parts[0] == 'f':
                    faces.append(list(map(int, [vertex.split('/')[0] for vertex in parts[1:]])))

    return vertices, faces

# Funktion zum Rendern der Szene
def render_scene(vertices, faces):
    glBegin(GL_TRIANGLES)
    for face in faces:
        for vertex_i in face:
            vertex = vertices[vertex_i - 1]
            glVertex3fv(vertex)
    glEnd()

# Funktion zum Setup der Beleuchtung
def setup_light():
    glEnable(GL_LIGHTING)
    
    # Ambient Light für weiche Schatten
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.2, 0.2, 0.2, 1.0))

    # Lichtquelle von oben
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (0, 1, 0, 0))  # Ändere die Position auf (0, 1, 0, 0) für Licht von oben
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1))
    glLightfv(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)  # Erhöhe den Wert für stärkeres Licht

# Funktion zum Hauptprogramm
def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    setup_light()  # Setup der Beleuchtung

    # Lade die OBJ-Datei
    vertices, faces = load_obj("3DModels/passat_low.obj")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Rendere die Szene
        render_scene(vertices, faces)

        glRotatef(1, 1, 3, 1)

        pygame.display.flip()

if __name__ == "__main__":
    main()
