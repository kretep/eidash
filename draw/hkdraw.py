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

    def __init__(self, width, height, font_dir='fonts'):
        self.context = DrawContext(width, height)
        self.context.font_normal = ImageFont.truetype(os.environ['NSDASH_FONT'], size=30)
        self.context.font_small = ImageFont.truetype(os.environ['NSDASH_FONT'], size=18)
        self.context.font_time = self.context.font_normal
        self.context.font_weather_icons = ImageFont.truetype(os.path.join(font_dir, 'weather-iconic.ttf'), size=80)
        self.context.font_icons_small = ImageFont.truetype(os.path.join(font_dir, 'weather-iconic.ttf'), size=40)

    def clear_image(self):
        self.context.draw.rectangle((0, 0, self.context.width, 
            self.context.height), fill=self.context.white)
        
    def draw_data(self, data):
        context = self.context

        # Clear
        self.clear_image()
        
        # Date & time
        draw_date(context, 10, 4)
        draw_time(context, self.context.width - 4, 4)
        
        # Weather
        y1 = 60
        weatherData = data["weather"]
        draw_current(context, 120, y1, 140, 80, weatherData)
        draw_temp(context, 260, y1, 140, 64, weatherData)
        draw_wind(context, 400, y1, 140, 80, 28, weatherData)
        isWarningActive = weatherData["alarm"] == "1"
        forecast_x = 10 if isWarningActive else 120
        draw_forecast(context, forecast_x, y1 + 110, 400, 0, weatherData)
        draw_forecast_table(context, forecast_x, 240, 100, 30, weatherData)
        if isWarningActive:
            draw_warning(context, forecast_x + 400, 150, 790 - forecast_x - 400, 200, weatherData)

        # Moon
        ephemData = data["ephem"]
        draw_moon_phase(context, 748, 80, 36, ephemData)

        # Sunspots
        draw_sunspots(context, 10, 80-36, 72, 72, data["sunspots"])

        # Nightscout
        nightScoutData = data["nightscout"]
        if not isWarningActive:
            # Normal case
            draw_nightscout(context, 650, self.context.height-36-10, 300, 100, nightScoutData)
        else:
            # Warning gets in the way
            draw_nightscout(context, 500, 10, 150, 100, nightScoutData)

        # Birthdays
        birthdayData = data["birthdays"]
        draw_birthdays(context, 10, self.context.height-28, birthdayData)
