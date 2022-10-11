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
        context.draw_dashed_line(p1[0], p1[1], p2[0], p2[1], 2)

    # Horizon
    positions = data["horizon"]
    for i in range(len(positions) - 1):
        i2 = i + 1
        p1 = equatorial_to_pixel(positions[i][0], positions[i][1])
        p2 = equatorial_to_pixel(positions[i2][0], positions[i2][1])
        if (p1[0] > p2[0]):
            # Wrapping line segment, draw at both ends
            context.draw_bounded_line((p1[0] - 600, p1[1]), p2, x, y, w, h)
            context.draw_bounded_line(p1, (p2[0] + 600, p2[1]), x, y, w, h)
        else:
            context.draw_bounded_line(p1, p2, x, y, w, h)

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
        context.draw_dashed_line(xc, y, xc, y + h, 20)
        context.draw.text((xc - 10, y + h), ["mrt", "jun", "sep", "dec", "mrt"][i], font=context.font_small)
