import os
from utils.utilities import incrementString
from utils.getGeo import get_maxspeed, get_location

class GeoController:

    def __init__(self):
        self.latitude = 0
        self.longitude = 0
        self.height = 0
        self.location = ""
        self.speed_limit = ""

        self.oxts_path = os.path.join("data", "Live", "oxts", "data")

        self.current_frame = "0000000000"

    def get_data(self):
        file_path = os.path.join(self.oxts_path, self.current_frame + ".txt")

        with open(file_path, 'r') as file:
            first_line = file.readline()

        oxts = [float(zahl) for zahl in first_line.split()[:3]]
        self.latitude, self.longitude, self.height = oxts

        next_frame = incrementString(self.current_frame)
        file_path = os.path.join(self.oxts_path, next_frame + ".txt")
        if os.path.exists(file_path):
            self.current_frame = next_frame

        #self.location = str(get_location(self.latitude, self.longitude))
        #self.speed_limit = str(get_maxspeed(str(self.latitude), str(self.longitude), str(100)))
       

    def update(self):
        self.get_data()
        return self.latitude, self.longitude, self.height, self.location, self.speed_limit


