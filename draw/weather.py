import os
import math
import numpy as np

black = 0
white = 1

wind_dir_names = ["Zuid", "ZZO", "ZO", "OZO", "Oost", "ONO", "NO", "NNO", 
        "Noord", "NNW", "NW", "WNW", "West", "WZW", "ZW", "ZZW"]

def draw_wind(draw, x, y, w, h, font, data):
    # Text
    text = f'{data["windr"]} {data["winds"]}'
    text_dim = draw.textsize(text, font)
    draw.text((x, y+h-text_dim[1]), text, font=font)
    
    # Arrow
    windr = data["windr"]
    if windr in wind_dir_names:
        angle = wind_dir_names.index(windr) / len(wind_dir_names) * 360
        draw_arrow(draw, x, y, w, angle, 3)

def draw_arrow(draw, x, y, d, angle, line_width):
    phi = angle / 360 * 2 * math.pi
    rotate = np.array([
        [math.cos(phi), math.sin(phi), 0],
        [-math.sin(phi), math.cos(phi), 0],
        [0, 0, 1]
    ])
    scale_translate = np.array([
        [d, 0, x + d/2],
        [0, d, y + d/2],
        [0, 0, 1]
    ])
    pts = np.array([
        (0.0, -0.4, 1),
        (0.2, 0.4, 1),
        (0.0, 0.2, 1),
        (-0.2, 0.4, 1)
    ])
    pts = np.einsum('rc,pc->pr', rotate, pts)
    pts = np.einsum('rc,pc->pr', scale_translate, pts)
    pts = [tuple(p[:-1]) for p in pts]
    draw.polygon(pts, outline=black, fill=None)
    draw.line([*pts, pts[0]], width=line_width, fill=black)
    map(lambda p: draw.circle(p, d/2, black), pts)

def draw_temp(draw, x, y, w, h, font, font2, data):
    text = f'{data["temp"]}°C'
    text_dim = draw.textsize(text, font)
    draw.text((x, y), text, font=font)
    text2 = f'gevoel {data["gtemp"]}°C'
    draw.text((x, y+text_dim[1]+4), text2, font=font2)

def draw_forecast(draw, image_text, x, y, w, h, font, data):
    text = data["verw"]
    image_text.write_text_box((x, y), text, box_width=w, \
        font_filename=os.environ['NSDASH_FONT'], font_size=18, color=black)

def draw_warning(draw, image_text, x, y, w, h, font, data):
    text = data["alarmtxt"]
    image_text.write_text_box((x,y), text, box_width=w, \
        font_filename=os.environ['NSDASH_FONT'], font_size=18, color=black)
