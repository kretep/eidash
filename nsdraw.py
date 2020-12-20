from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os

black = 0
white = 1

class NSDraw:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.image = Image.new('1', (width, height), white)
        self.draw = ImageDraw.Draw(self.image)

        self.font = ImageFont.truetype(os.environ['NSDASH_FONT'], size=42)
        self.font2 = ImageFont.truetype(os.environ['NSDASH_FONT'], size=20)

    def clear_image(self):
        self.draw.rectangle((0, 0, self.width, self.height), fill=white)
        
    def draw_data(self, data):
        draw = self.draw

        # Clear
        self.clear_image()
        
        # Main value
        main_text = f'{data["sgv"]}{data["direction"]}'
        draw.text((20, 20), main_text, font = self.font, fill = black)

        # Delta
        main_size = draw.textsize(main_text, self.font)
        delta_text = f'{data["delta"]}\n[{data["minutes_ago"]}m]'
        draw.text((20 + main_size[0], 20), delta_text, font=self.font2, fill=black)
        
        # Draw time
        time_text = datetime.now().strftime("%H:%M")
        time_dim = draw.textsize(time_text, self.font2)
        draw.text((self.width - time_dim[0], 0), time_text, font=self.font2)
