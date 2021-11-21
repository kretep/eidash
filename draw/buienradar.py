from math import sin, cos, pi, pow

def draw_buienradar_chart(context, x, y, w, h, data):
    context.draw.rectangle((x, y+h, x+w, y))
    n = len(data) - 1
    pts = [(x + int(1.0 * w * i / n), y+h - int(1.0 * h * float(p[1]) / 255)) for i, p in enumerate(data)]
    context.draw.line(pts, width=3, fill=context.black)
    draw_raindrop(context, x + w / 2, y + h / 3, 5)

def draw_raindrop(context, xc, yc, r):
    # Generate curve
    n = 25
    segments = [[], [], []]
    for i in range(n):
        t = 1.0 / n * i
        # https://www.desmos.com/calculator/5pwkmxjsyg
        segments[0].append( (xc - (1 - pow(t, 2)) * r * cos(pi / 2 * t), yc - (1 - pow(t, 2)) * r * sin(pi / 2 * t) - pow(t, 2) * r * 2.5 * t) )
        segments[1].append( (xc + (1 - pow(t, 2)) * r * cos(pi / 2 * t), yc - (1 - pow(t, 2)) * r * sin(pi / 2 * t) - pow(t, 2) * r * 2.5 * t) )
        segments[2].append( (xc + r * cos(pi * t), yc + r * sin(pi * t)) )
    segments[1].reverse()
    points = segments[0] + segments[1] + segments[2] + [segments[0][0]]

    # Round coordinates (really improves curve accuracy)
    points = list(map(lambda pair: (round(pair[0]), round(pair[1])), points))

    # Draw curve
    context.draw.line(points, width=1, fill=context.black)
