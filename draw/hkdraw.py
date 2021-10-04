from draw.drawcontext import DrawContext
from PIL import Image, ImageDraw, ImageFont
import os
from .date_time import *
from .moonphase import *
from .nightscout import *
from .weather import *
from .birthdays import *
from draw.sunspots import draw_sunspot_number, draw_sunspot_image
from .buienradar import draw_buienradar_chart
from .planets import draw_planets

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
        w1 = 140
        x1 = (self.context.width - 3 * w1) / 2
        weatherData = data["weather"]
        draw_current(context, x1, y1, w1, 80, weatherData)
        draw_temp(context, x1+w1, y1, w1, 64, weatherData)
        draw_wind(context, x1+2*w1, y1, w1, 80, 28, weatherData)
        isWarningActive = weatherData["alarm"] == "1"
        forecast_x = 10 if isWarningActive else 90
        draw_forecast_table(context, forecast_x, y1 + 110, 100, 30, weatherData)
        draw_forecast(context, forecast_x + 400, y1 + 110, 300, 0, weatherData)
        if isWarningActive:
            draw_warning(context, forecast_x + 400, 150, 790 - forecast_x - 400, 200, weatherData)

        # Buienradar
        draw_buienradar_chart(context, 10, 150, 74, 74, data["buienradar_text"])

        # Moon phase and planets
        ephemData = data["ephem"]
        draw_moon_phase(context, 748, 80, 36, ephemData)
        draw_planets(context, 10, 330, 600, 130, ephemData)

        # Sunspots
        draw_sunspot_image(context, 10, 80-36, 72, 72, data["sunspot_image"])
        draw_sunspot_number(context, 10, 120, 72, 20, data["sunspot_number"])

        # Nightscout
        nightScoutData = data["nightscout"]
        if not isWarningActive:
            # Normal case
            draw_nightscout(context, 650, self.context.height-36-10, 150, 36+10, nightScoutData)
        else:
            # Warning gets in the way
            draw_nightscout(context, 500, 10, 150, 100, nightScoutData)

        # Birthdays
        birthdayData = data["birthdays"]
        draw_birthdays(context, 100, y1-20, birthdayData)
