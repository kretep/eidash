from PIL import Image, ImageDraw, ImageFont
from lib.image_text import ImageText
import os
from .date_time import *
from .moonphase import *
from .nightscout import *
from .weather import *
from .birthdays import *
from draw.sunspots import draw_sunspots

black = 0
white = 1

class HKDraw:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.image = Image.new('1', (width, height), white)
        self.draw = ImageDraw.Draw(self.image)
        self.image_text = ImageText(self.image, self.draw)

        self.font = ImageFont.truetype(os.environ['NSDASH_FONT'], size=30)
        self.font2 = ImageFont.truetype(os.environ['NSDASH_FONT'], size=18)

    def clear_image(self):
        self.draw.rectangle((0, 0, self.width, self.height), fill=white)
        
    def draw_data(self, data):
        draw = self.draw

        # Clear
        self.clear_image()
        
        # Date & time
        draw_date(draw, 10, 4, self.font)
        draw_time(draw, self.width - 4, 4, self.font)
        
        # Weather
        y1 = 50
        weatherData = data["weather"]
        draw_wind(draw, 110, y1, 64, 80, self.font2, weatherData)
        draw_temp(draw, 200, y1, 80, 80, self.font, self.font2, weatherData)
        draw_forecast(draw, self.image_text, 110, y1+84, 400, 0, self.font2, weatherData)
        if weatherData["alarm"] == "1":
            draw_warning(draw, self.image_text, 10, 150, 700, 200, self.font2, weatherData)
        
        # Moon
        ephemData = data["ephem"]
        draw_moon_phase(draw, 748, 80, 36, ephemData)

        # Sunspots
        draw_sunspots(self.image, 10, 80-36, 72, 72, data["sunspots"])

        # Nightscout
        nightScoutData = data["nightscout"]
        draw_nightscout(draw, 650, 150, 300, 100, self.font, self.font2, nightScoutData)

        # Birthdays
        birthdayData = data["birthdays"]
        draw_birthdays(draw, 10, self.height-50, self.font2, birthdayData)
