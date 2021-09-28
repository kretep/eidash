from .moonphase import draw_moon_phase

def draw_planets(context, x, y, w, h, data):
    positions = data["positions"]
    context.draw.rectangle((x, y, x+w, y+h))
    for key, value in positions.items():
        xc = x+w - 1.0 * w * value[0] / 360
        yc = y+0.5*h - 0.5 * h * value[1] / 28
        r = 2
        if key == 'Sun':
            r = 6
            context.draw.ellipse((xc - r, yc - r, xc + r, yc + r), fill=context.white, outline=context.black, width=2)
        elif key == "Moon":
            r = 6
            draw_moon_phase(context, xc, yc, r, data, line_width=1)
        else:
            context.draw.ellipse((xc - r, yc - r, xc + r, yc + r), fill=context.black)
            symbol = key[0] if key != 'Mercury' else 'm'
            context.draw.text((xc + r, yc + r), symbol, font=context.font_small)
