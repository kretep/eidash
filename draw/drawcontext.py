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

    def draw_dashed_line(self, x1, y1, x2, y2, steps):
        xd = (x2 - x1) / steps
        yd = (y2 - y1) / steps
        for i in range(steps):
            self.draw.line((x1 + xd * i, y1 + yd * i, x1 + xd * (i + 0.5), y1 + yd * (i + 0.5)))

    def draw_bounded_line(self, p1, p2, bx, by, bw, bh):
        p1_inside = p1[0] >= bx and p1[0] <= bx + bw and p1[1] >= by and p1[1] <= by + bh
        p2_inside = p2[0] >= bx and p2[0] <= bx + bw and p2[1] >= by and p2[1] <= by + bh
        if not p1_inside and not p2_inside:
            # we're assuming a short line segment that doesn't cross the box entirely
            # (which would be ignored here)
            return
        if p1_inside and p2_inside:
           self.draw.line((p1[0], p1[1], p2[0], p2[1]))
           return

        def ccw(p1, p2, p3):
            return (p3[1]-p1[1]) * (p2[0]-p1[0]) > (p2[1]-p1[1]) * (p3[0]-p1[0])

        def draw_on_intersect(p1, p2, p3, p4):
            its = self.intersect(p1, p2, p3, p4)
            if not its is None:
                if ccw(p1, p3, p4):
                    self.draw.line((p1[0], p1[1], its[0], its[1]))
                else:
                    self.draw.line((p2[0], p2[1], its[0], its[1]))

        draw_on_intersect(p1, p2, (bx, by), (bx + bw, by))
        draw_on_intersect(p1, p2, (bx + bw, by), (bx + bw, by + bh))
        draw_on_intersect(p1, p2, (bx + bw, by + bh), (bx, by + bh))
        draw_on_intersect(p1, p2, (bx, by + bh), (bx, by))

    # intersection between line(p1, p2) and line(p3, p4)
    def intersect(self, p1, p2, p3, p4):
        x1,y1 = p1
        x2,y2 = p2
        x3,y3 = p3
        x4,y4 = p4
        denom = (y4-y3)*(x2-x1) - (x4-x3)*(y2-y1)
        if denom == 0: # parallel
            return None
        ua = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / denom
        if ua < 0 or ua > 1: # out of range
            return None
        ub = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / denom
        if ub < 0 or ub > 1: # out of range
            return None
        x = x1 + ua * (x2-x1)
        y = y1 + ua * (y2-y1)
        return (x,y)
