import os
from utils.utilities import incrementString
from utils.getGeo import get_maxspeed, get_location
from configs.settings import base_directory, start_frame

class GeoController:

    def __init__(self):
        self.latitude = 0
        self.longitude = 0
        self.height = 0

        self.oxts_path = os.path.join(base_directory, "oxts", "source")

        self.current_frame = start_frame

    def get_data(self):
        file_path = os.path.join(self.oxts_path, self.current_frame + ".txt")

        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                first_line = file.readline()

            oxts = [float(zahl) for zahl in first_line.split()[:3]]
            self.latitude, self.longitude, self.height = oxts

            next_frame = incrementString(self.current_frame)
            file_path = os.path.join(self.oxts_path, next_frame + ".txt")
            if os.path.exists(file_path):
                self.current_frame = next_frame
        else:
            print(f"no data for GPS at: {file_path}")
            self.latitude = -1
            self.longitude = -1
            self.height = -1
            self.current_frame = start_frame


    def update(self):
        self.get_data()
        return self.latitude, self.longitude, self.height


