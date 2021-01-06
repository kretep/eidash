from draw.drawcontext import DrawContext
from PIL import ImageFont
import os
from .date_time import *
from .nightscout import *

class NSDraw:

    def __init__(self, width, height):
        self.context = DrawContext(width, height)
        self.context.font_normal = ImageFont.truetype(os.environ['NSDASH_FONT'], size=36)
        self.context.font_small = ImageFont.truetype(os.environ['NSDASH_FONT'], size=18)

    def draw_data(self, data):
        self.context.clear_image()
        draw_time(self.context, self.context.width - 4, 4, self.context.font_small)
        draw_nightscout(self.context, 10, 10, 150, 100, data)
