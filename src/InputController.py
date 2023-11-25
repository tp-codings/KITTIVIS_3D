import pygame
from pygame.locals import DOUBLEBUF, OPENGL, MOUSEBUTTONDOWN, MOUSEBUTTONUP


class InputController:
    def __init__(self):
        self.dragging = False;
        self.zoom_factor = 1.0
        self.initial_mouse_pos = None
        self.stop = False
        

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop = True
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # left mouse button
                    self.dragging = True
                    self.initial_mouse_pos = pygame.mouse.get_pos()
                if event.button == 4:  # scroll wheel up
                    self.zoom_factor /= 1.3
                if event.button == 5:  # scroll wheel down
                    self.zoom_factor *= 1.3

            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:  # left mouse button
                    self.dragging = False
                    self.initial_mouse_pos = None
        #print(self.dragging, self.initial_mouse_pos, self.zoom_factor)
        return self.stop, self.initial_mouse_pos, self.zoom_factor, self.dragging