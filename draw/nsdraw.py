from draw.drawcontext import DrawContext
from PIL import ImageFont
import os
from .date_time import *
from .nightscout import *

class NSDraw:

    def __init__(self, width, height):
        self.context = DrawContext(width, height)
        self.context.font_normal = ImageFont.truetype(os.environ['NSDASH_FONT'], size=76)
        self.context.font_small = ImageFont.truetype(os.environ['NSDASH_FONT'], size=28)
        self.context.font_time = ImageFont.truetype(os.environ['NSDASH_FONT'], size=28)

    def draw_data(self, data):
        context = self.context
        context.clear_image()

        minutes_ago = data["minutes_ago"]
        minutes_ago_text = str(minutes_ago) if minutes_ago >= 0 else "?"
        time_text = datetime.now().strftime("%H:%M")
        delta_text = f'{data["delta"]}|{minutes_ago_text}m {time_text}'
        main_text = f'{data["sgv"]}{data["direction"]}'

        # Determine text size and layout
        delta_size = context.draw.textsize(delta_text, context.font_small)
        main_size = context.draw.textsize(main_text, context.font_normal)
        w = context.width
        delta_x = (w - delta_size[0]) / 2
        delta_y = 4 # margin
        main_x = (w - main_size[0]) / 2
        main_y = delta_y + delta_size[1]

        # Draw
        context.draw.text((delta_x, delta_y), delta_text, font=context.font_small, fill=context.black)
        context.draw.text((main_x, main_y), main_text, font=context.font_normal, fill=context.black)

        # Strikethrough for old data
        if minutes_ago > 8:
            y = main_y + main_size[1] / 2 + 4
            context.draw.line([(main_x, y), (main_x + main_size[0], y)], 
                width=8, fill=context.black)
