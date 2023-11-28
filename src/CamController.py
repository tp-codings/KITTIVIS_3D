import os
import pygame
from utils.utilities import incrementString
from utils.settings import colors
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from ultralytics import YOLO


class CamController:

    def __init__(self, display):
        self.base_path = os.path.join("data", "Live")
        self.cam_paths = [os.path.join(self.base_path, f"image_{i:02d}", "data") for i in range(3, 4)]

        self.current_frame = "0000000000"

        self.cams = [None]
        self.texture_ids = [None]

        self.positions = [(50, display[1] / 2-100)]

        self.model = YOLO("YoloWeights/yolov8l.pt")
        self.classNames = self.model.names

        self.detections = []

    def get_data(self):
        for i, cam_path in enumerate(self.cam_paths):
            file_path = os.path.join(cam_path, f"{self.current_frame}.png")
            self.cams[i] = pygame.image.load(file_path).convert()
            


        next_frame = incrementString(self.current_frame)
        if all(os.path.exists(os.path.join(cam_path, f"{next_frame}.png")) for cam_path in self.cam_paths):
            self.current_frame = next_frame

    def load_texture(self, cam_index):
        cam = self.cams[cam_index]
        width, height = cam.get_width(), cam.get_height()
        texture_data = pygame.image.tostring(cam, "RGBA", True)

        if self.texture_ids[cam_index] is None:
            self.texture_ids[cam_index] = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, self.texture_ids[cam_index])
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    def perform_yolo_detection(self, cam_index):
        imgdata = pygame.surfarray.array3d(self.cams[cam_index])
        imgdata = imgdata.swapaxes(0, 1)
        results = self.model(imgdata, stream=True, verbose=False)
        
        temp_detect = []
        image_height = imgdata.shape[0]
        
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls = self.classNames[int(box.cls[0])]
                
                # Spiegle die Bounding Boxes vertikal
                flipped_y1 = image_height - y2
                flipped_y2 = image_height - y1
                
                temp_detect.append((x1, flipped_y1, x2, flipped_y2, cls))
        
        self.detections = temp_detect

    def update(self):
        self.get_data()
        self.perform_yolo_detection(0)
        for i in range(len(self.cams)):
            self.load_texture(i)

    def render(self, scale=0.5):
        glPushAttrib(GL_CURRENT_BIT)
        glBegin(GL_LINES)

        for rect in self.detections:
            cls = rect[4]
            scaled_rect = [rect[i] * scale for i in range(4)]
            x1, y1, x2, y2 = scaled_rect
            color=colors.get(cls.lower(), (1.0, 1.0, 1.0))
            glColor3fv(color)

            x, y = self.positions[0]
            x = x / 20
            y = y / 20
            shift_vector = (x, y)

            glVertex2f((x1 / 20) + shift_vector[0], (y1 / 20) + shift_vector[1])
            glVertex2f((x2 / 20) + shift_vector[0], (y1 / 20) + shift_vector[1])

            glVertex2f((x2 / 20) + shift_vector[0], (y1 / 20) + shift_vector[1])
            glVertex2f((x2 / 20) + shift_vector[0], (y2 / 20) + shift_vector[1])

            glVertex2f((x2 / 20) + shift_vector[0], (y2 / 20) + shift_vector[1])
            glVertex2f((x1 / 20) + shift_vector[0], (y2 / 20) + shift_vector[1])

            glVertex2f((x1 / 20) + shift_vector[0], (y2 / 20) + shift_vector[1])
            glVertex2f((x1 / 20) + shift_vector[0], (y1 / 20) + shift_vector[1])
        glEnd()
        glPopAttrib()

        for i, position in enumerate(self.positions):
            x, y = position

            width, height = self.cams[i].get_width(), self.cams[i].get_height()

            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_ids[i])

            tr = (x / 20 + width * scale / 20, y / 20 + height * scale / 20)
            tl = (x / 20, y / 20 + height * scale / 20)

            bl = (x / 20, y / 20)
            br = (x / 20 + width * scale / 20, y / 20)


            glBegin(GL_QUADS)
            glTexCoord2f(1, 0)  # Unten links
            glVertex2f(br[0], br[1])

            glTexCoord2f(0, 0)  # Unten rechts
            glVertex2f(bl[0], bl[1])

            glTexCoord2f(0, 1)  # Oben rechts
            glVertex2f(tl[0], tl[1])

            glTexCoord2f(1, 1)  # Oben links
            glVertex2f(tr[0], tr[1])
            glEnd()

            glDisable(GL_TEXTURE_2D)

            glDeleteTextures([self.texture_ids[i]])
