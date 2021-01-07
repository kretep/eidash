from draw.drawcontext import DrawContext
from PIL import Image, ImageDraw, ImageFont
import os
from .date_time import *
from .moonphase import *
from .nightscout import *
from .weather import *
from .birthdays import *
from draw.sunspots import draw_sunspots


class HKDraw:

    def __init__(self, width, height):
        self.context = DrawContext(width, height)
        self.context.font_normal = ImageFont.truetype(os.environ['NSDASH_FONT'], size=30)
        self.context.font_small = ImageFont.truetype(os.environ['NSDASH_FONT'], size=18)
        self.context.font_weather_icons = ImageFont.truetype(os.path.join('fonts', 'weather-iconic.ttf'), size=80)
        self.context.font_icons_small = ImageFont.truetype(os.path.join('fonts', 'weather-iconic.ttf'), size=40)

    def clear_image(self):
        self.context.draw.rectangle((0, 0, self.context.width, 
            self.context.height), fill=self.context.white)
        
    def draw_data(self, data):
        context = self.context

        # Clear
        self.clear_image()
        
        # Date & time
        draw_date(context, 10, 4)
        draw_time(context, self.context.width - 4, 4, context.font_normal)
        
        # Weather
        y1 = 50
        weatherData = data["weather"]
        draw_current(context, 120, y1, 140, 80, weatherData)
        draw_temp(context, 260, y1, 80, 80, weatherData)
        draw_wind(context, 400, y1, 64, 80, weatherData)
        draw_forecast(context, 120, y1+84, 400, 0, weatherData)
        draw_forecast_table(context, 120, 200, 100, 30, weatherData)
        if weatherData["alarm"] == "1":
            draw_warning(context, 10, 150, 700, 200, weatherData)
        
        # Moon
        ephemData = data["ephem"]
        draw_moon_phase(context, 748, 80, 36, ephemData)

        # Sunspots
        draw_sunspots(context, 10, 80-36, 72, 72, data["sunspots"])

        # Nightscout
        nightScoutData = data["nightscout"]
        draw_nightscout(context, 650, self.context.height-100, 300, 100, nightScoutData)

        # Birthdays
        birthdayData = data["birthdays"]
        draw_birthdays(context, 10, self.context.height-50, birthdayData)
