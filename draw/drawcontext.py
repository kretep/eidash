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

    def draw_circle(self, coords, r, *args, **kwargs):
        x, y = coords
        self.draw.ellipse((x - r, y - r, x + r, y + r), *args, **kwargs)

    def draw_pretty_polygon(self, points, line_width, outline=0, fill=1):
        # Draw the filled polygon first
        self.draw.polygon(points, outline=outline, fill=fill)

        # Draw the outline
        self.draw.line([*points, points[0]], width=line_width, fill=outline)

        # Rounded connectors
        for p in points:
            self.draw_circle(p, line_width/3, fill=outline)
