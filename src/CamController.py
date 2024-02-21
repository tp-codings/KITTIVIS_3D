import os
import pygame
from utils.utilities import incrementString
from configs.settings import colors, base_directory, start_frame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from ultralytics import YOLO
import torch


class CamController:

    def __init__(self, display):
        self.cam_paths = [os.path.join(base_directory, f"image_{i:02d}", "source") for i in range(3, 4)]
        self.current_frame = start_frame
        self.cams = [None for x in range(len(self.cam_paths))]
        self.texture_ids = [None for x in range(len(self.cam_paths))]
        self.positions = [(50, display[1] / 2-5)] #hier obacht
        self.model = YOLO("YoloWeights/yolov8n.pt")
        self.classNames = self.model.names
        self.detections = []
        print("Cuda Available: ", torch.cuda.is_available())

    def get_data(self):
        for i, cam_path in enumerate(self.cam_paths):
            file_path = os.path.join(cam_path, f"{self.current_frame}.png")

            if os.path.exists(file_path):
                self.cams[i] = pygame.image.load(file_path).convert()
            else:
                #print(f"no data for cam0{i} at: {file_path}")
                self.cams[i] = None
                self.current_frame = start_frame


        next_frame = incrementString(self.current_frame)
        if all(os.path.exists(os.path.join(cam_path, f"{next_frame}.png")) for cam_path in self.cam_paths):
            self.current_frame = next_frame

    def perform_yolo_detection(self, cam_index):
        imgdata = pygame.surfarray.array3d(self.cams[cam_index]).swapaxes(0, 1)
        results = self.model(imgdata, stream=True, verbose=False)
        
        temp_detect = []
        image_height = imgdata.shape[0]
        
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls = self.classNames[int(box.cls[0])]
                
                temp_detect.append((x1, image_height - y2, x2, image_height - y1, cls))
        
        self.detections = temp_detect

    def load_texture(self, cam_index):
        cam = self.cams[cam_index]
        width, height = cam.get_width(), cam.get_height()
        texture_data = pygame.image.tostring(cam, "RGBA", True)

        self.texture_ids[cam_index] = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_ids[cam_index])
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    def update(self):
        self.get_data()
        for i in range(len(self.cams)):
            if self.cams[i] is not None:
                #self.perform_yolo_detection(i)
                self.load_texture(i)

    def render(self, scale=0.5):
        glPushAttrib(GL_CURRENT_BIT)
        glBegin(GL_LINES)

        for rect in self.detections:
            cls = rect[4]
            scaled_rect = [coord * scale / 20 for coord in rect[:4]]
            x1, y1, x2, y2 = scaled_rect
            color = colors.get(cls.lower(), (1.0, 1.0, 1.0))
            glColor3fv(color)

            x, y = [coord / 20 for coord in self.positions[0]]
            shift_vector = (x, y)

            glVertex2f(x1 + shift_vector[0], y1 + shift_vector[1])
            glVertex2f(x2 + shift_vector[0], y1 + shift_vector[1])

            glVertex2f(x2 + shift_vector[0], y1 + shift_vector[1])
            glVertex2f(x2 + shift_vector[0], y2 + shift_vector[1])

            glVertex2f(x2 + shift_vector[0], y2 + shift_vector[1])
            glVertex2f(x1 + shift_vector[0], y2 + shift_vector[1])

            glVertex2f(x1 + shift_vector[0], y2 + shift_vector[1])
            glVertex2f(x1 + shift_vector[0], y1 + shift_vector[1])
        glEnd()
        glPopAttrib()

        for i, position in enumerate(self.positions):
            if self.cams[i] is not None:
                x, y = [coord / 20 for coord in position]

                width, height = self.cams[i].get_width() * scale / 20, self.cams[i].get_height() * scale / 20

                glEnable(GL_TEXTURE_2D)
                glBindTexture(GL_TEXTURE_2D, self.texture_ids[i])

                tr = (x + width, y + height)
                tl = (x, y + height)
                bl = (x, y)
                br = (x + width, y)

                glBegin(GL_QUADS)
                glTexCoord2f(1, 0)
                glVertex2f(br[0], br[1])

                glTexCoord2f(0, 0)
                glVertex2f(bl[0], bl[1])

                glTexCoord2f(0, 1)
                glVertex2f(tl[0], tl[1])

                glTexCoord2f(1, 1)
                glVertex2f(tr[0], tr[1])
                glEnd()

                glDisable(GL_TEXTURE_2D)
                glDeleteTextures([self.texture_ids[i]])
