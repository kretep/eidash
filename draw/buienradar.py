
def draw_buienradar_chart(context, x, y, w, h, data):
    context.draw.rectangle((x, y+h, x+w, y))
    n = len(data) - 1
    pts = [(x + int(1.0 * w * i / n), y+h - int(1.0 * h * int(p[1]) / 255)) for i, p in enumerate(data)]
    context.draw.line(pts, width=3, fill=context.black)
