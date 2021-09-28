from .moonphase import draw_moon_phase

def draw_planets(context, x, y, w, h, data):

    def equatorial_to_pixel(ra, dec):
        return (x+w - 1.0 * w * ra / 360, y+0.5*h - 0.5 * h * dec / 28)

    # Sun position over the year
    positions = data["sun_positions"]
    for i in range(len(positions) - 1):
        i2 = i + 1
        p1 = equatorial_to_pixel(positions[i][0], positions[i][1])
        p2 = equatorial_to_pixel(positions[i2][0], positions[i2][1])
        context.draw.line((p1[0], p1[1], p2[0], p2[1]))

    # Planets
    positions = data["positions"]
    context.draw.rectangle((x, y, x+w, y+h))
    for key, value in positions.items():
        xc, yc = equatorial_to_pixel(*value)
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

    # Calendar lines
    for i in range(5):
        xc = x+w - 1.0 * w * i / 4
        #context.draw.line((xc, y, xc, y + h))
        draw_dashed_line(context, xc, y, xc, y + h, 20)
        context.draw.text((xc - 10, y + h), ["mrt", "jun", "sep", "dec", "mrt"][i], font=context.font_small)

def draw_dashed_line(context, x1, y1, x2, y2, steps):
    xd = (x2 - x1) / steps
    yd = (y2 - y1) / steps
    for i in range(steps):
        context.draw.line((x1 + xd * i, y1 + yd * i, x1 + xd * (i + 0.5), y1 + yd * (i + 0.5)))

