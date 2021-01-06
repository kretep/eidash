import os
import math
import numpy as np

weather_icons = {
    "zonnig": "\ue92c",
    "bliksem": "\ue918",
    "regen": "\ue905",
    "buien": "\ue906",
    "hagel": "\ue917",
    "mist": "\ue916",
    "sneeuw": "\ue92b",
    "bewolkt": "\ue902",
    "halfbewolkt": "\ue92d",
    "zwaarbewolkt": "\ue90b",
    "nachtmist": "\ue920",
    "helderenacht": "\ue926",
    "wolkennacht": "\ue91a",
}

def draw_current(context, x, y, w, h, data):
    # Text
    text = data["samenv"]
    text_dim = context.draw.textsize(text, context.font_small)
    context.image_text.write_text_box((x,y+h-2*text_dim[1]), text, box_width=w, \
        font_filename=os.environ['NSDASH_FONT'], font_size=18, color=context.black)

    # Icon
    icon_text = weather_icons[data["image"]]
    icon_dim = context.draw.textsize(icon_text, font=context.font_weather_icons)
    context.draw.text((x + w/2 - icon_dim[0]/2, y-10), icon_text, 
        font=context.font_weather_icons)

wind_dir_names = ["Zuid", "ZZO", "ZO", "OZO", "Oost", "ONO", "NO", "NNO", 
        "Noord", "NNW", "NW", "WNW", "West", "WZW", "ZW", "ZZW"]
wind_dir_names_verw = ["Z", "ZZO", "ZO", "OZO", "O", "ONO", "NO", "NNO", 
        "N", "NNW", "NW", "WNW", "W", "WZW", "ZW", "ZZW"] # and VAR for variable

def draw_wind(context, x, y, w, h, data):
    # Text
    text = f'{data["windr"]} {data["winds"]}'
    text_dim = context.draw.textsize(text, context.font_small)
    context.draw.text((x, y+h-text_dim[1]), text, font=context.font_small)
    
    # Arrow
    windr = data["windr"]
    if windr in wind_dir_names:
        angle = wind_dir_names.index(windr) / len(wind_dir_names) * 360
        draw_arrow(context, x, y, w, angle, 3)

def draw_arrow(context, x, y, d, angle, line_width):
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
    context.draw.polygon(pts, outline=context.black, fill=None)
    context.draw.line([*pts, pts[0]], width=line_width, fill=context.black)
    map(lambda p: context.draw.circle(p, d/2, context.black), pts)

def draw_temp(context, x, y, w, h, data):
    text = f'{data["temp"]}°C'
    text_dim = context.draw.textsize(text, context.font_normal)
    context.draw.text((x, y), text, font=context.font_normal)
    text2 = f'gevoel {data["gtemp"]}°C'
    context.draw.text((x, y+text_dim[1]+4), text2, font=context.font_small)

def draw_forecast(context, x, y, w, h, data):
    text = f'Verw: {data["verw"]}'
    context.image_text.write_text_box((x, y), text, box_width=w, \
        font_filename=os.environ['NSDASH_FONT'], font_size=18, color=context.black)

def draw_warning(context, x, y, w, h, data):
    text = data["alarmtxt"]
    context.image_text.write_text_box((x,y), text, box_width=w, \
        font_filename=os.environ['NSDASH_FONT'], font_size=18, color=context.black)
