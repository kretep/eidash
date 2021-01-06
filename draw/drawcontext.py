from PIL import Image, ImageDraw
from lib.image_text import ImageText

class DrawContext:

    def __init__(self, width, height):
        self.black = 0
        self.white = 1
        self.width = width
        self.height = height
        self.image = Image.new('1', (width, height), self.white)
        self.draw = ImageDraw.Draw(self.image)
        self.image_text = ImageText(self.image, self.draw)

    def clear_image(self):
        self.draw.rectangle((0, 0, self.width, self.height), fill=self.white)
