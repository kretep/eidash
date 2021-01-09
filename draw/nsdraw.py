from draw.drawcontext import DrawContext
from PIL import ImageFont
import os
from .date_time import *
from .nightscout import *

class NSDraw:

    def __init__(self, width, height):
        self.context = DrawContext(width, height)
        self.context.font_normal = ImageFont.truetype(os.environ['NSDASH_FONT'], size=54)
        self.context.font_small = ImageFont.truetype(os.environ['NSDASH_FONT'], size=27)
        self.context.font_time = ImageFont.truetype(os.environ['NSDASH_FONT'], size=18)

    def draw_data(self, data):
        self.context.clear_image()
        draw_time(self.context, self.context.width - 4, 4)
        y = (self.context.height - self.context.font_normal.size) / 2
        draw_nightscout(self.context, 0, y, self.context.width, 100, data)
