import math

black = 0
white = 1

def draw_moon_phase(draw, x, y, r, data):
    f = data["moon_age_fraction"] # value between 0 and 1, where 0.5=full moon
    b = 1
    r2 = r + b

    if 0.0 <= f < 0.25:
        draw.ellipse([x-r2, y-r2, x+r2, y+r2], fill=white, outline=black)
        terminator = r * math.cos(f * 2 * math.pi)
        draw.ellipse([x-terminator, y-r, x+terminator, y+r], fill=black, outline=black)
        draw.chord([x-r2, y-r2, x+r2, y+r2], 90, 270, fill=black, outline=black)
    elif 0.25 <= f < 0.5:
        draw.ellipse([x-r2, y-r2, x+r2, y+r2], fill=black, outline=black)
        terminator = r * math.cos(f * 2 * math.pi)
        draw.ellipse([x+terminator, y-r, x-terminator, y+r], fill=white, outline=white)
        draw.chord([x-r, y-r, x+r, y+r], 270, 90, fill=white, outline=white)
    elif 0.5 <= f < 0.75:
        draw.ellipse([x-r2, y-r2, x+r2, y+r2], fill=black, outline=black)
        terminator = r * math.cos(f * 2 * math.pi - math.pi)
        draw.ellipse([x-terminator, y-r, x+terminator, y+r], fill=white, outline=white)
        draw.chord([x-r, y-r, x+r, y+r], 90, 270, fill=white, outline=white)
    elif 0.75 <= f <= 1.0:
        draw.ellipse([x-r2, y-r2, x+r2, y+r2], fill=white, outline=black)
        terminator = r * math.cos(f * 2 * math.pi - math.pi)
        draw.ellipse([x+terminator, y-r, x-terminator, y+r], fill=black, outline=black)
        draw.chord([x-r2, y-r2, x+r2, y+r2], 270, 90, fill=black, outline=black)
