from PIL import Image, ImageDraw, ImageFont
import os
import draw_datetime, draw_nightscout

black = 0
white = 1

class NSDraw:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.image = Image.new('1', (width, height), white)
        self.draw = ImageDraw.Draw(self.image)

        self.font = ImageFont.truetype(os.environ['NSDASH_FONT'], size=36)
        self.font2 = ImageFont.truetype(os.environ['NSDASH_FONT'], size=18)

    def clear_image(self):
        self.draw.rectangle((0, 0, self.width, self.height), fill=white)
        
    def draw_data(self, data):
        self.clear_image()
        draw_datetime.draw_time(self.draw, self.width - 4, 4, self.font2)
        draw_nightscout.draw_nightscout(self.draw, 10, 10, 150, 100, self.font, self.font2, data)
