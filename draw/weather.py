import os
import math
import numpy as np
from datetime import datetime, timedelta

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
    "lichtbewolkt": "\ue92d",
    "zwaarbewolkt": "\ue90b",
    "nachtmist": "\ue920",
    "helderenacht": "\ue926",
    "wolkennacht": "\ue91a",
    "nachtbewolkt": "\ue91a",
}

def draw_current(context, x, y, w, h, data):
    # Icon
    icon_text = weather_icons.get(data["image"], "?")
    icon_dim = context.draw.textsize(icon_text, font=context.font_weather_icons)
    context.draw.text((x + w/2 - icon_dim[0]/2, y-10), icon_text, 
        font=context.font_weather_icons)

    # Text
    text = data["samenv"]
    text_dim = context.draw.textsize(text, context.font_small)
    context.image_text.write_text_box(x, y + h - context.font_small.size, text,
        box_width=2*w, font=context.font_small, color=context.black)

wind_dir_names = ["Zuid", "ZZO", "ZO", "OZO", "Oost", "ONO", "NO", "NNO", 
        "Noord", "NNW", "NW", "WNW", "West", "WZW", "ZW", "ZZW"]
wind_dir_names_verw = ["Z", "ZZO", "ZO", "OZO", "O", "ONO", "NO", "NNO", 
        "N", "NNW", "NW", "WNW", "W", "WZW", "ZW", "ZZW"] # and VAR for variable

def draw_wind(context, x, y, w, h, arrow_r, data):
    # Text
    text = f'{data["windr"]} {data["winds"]}'
    text_dim = context.draw.textsize(text, context.font_small)
    context.image_text.write_text_box(x, y + h - context.font_small.size, text, w,
        font=context.font_small, color=context.black, align='center')

    # Arrow
    windr = data["windr"]
    if windr in wind_dir_names:
        angle = wind_dir_names.index(windr) / len(wind_dir_names) * 360
        draw_arrow(context, x + w/2, y + arrow_r, arrow_r, angle, 3)

def draw_arrow(context, cx, cy, r, angle, line_width):
    phi = angle / 360 * 2 * math.pi
    rotate = np.array([
        [math.cos(phi), math.sin(phi), 0],
        [-math.sin(phi), math.cos(phi), 0],
        [0, 0, 1]
    ])
    scale_translate = np.array([
        [r, 0, cx],
        [0, r, cy],
        [0, 0, 1]
    ])
    pts = np.array([
        (0.0, -0.8, 1),
        (0.4, 0.8, 1),
        (0.0, 0.4, 1),
        (-0.4, 0.8, 1)
    ])
    pts = np.einsum('rc,pc->pr', rotate, pts)
    pts = np.einsum('rc,pc->pr', scale_translate, pts)
    pts = [tuple(p[:-1]) for p in pts]
    context.draw_pretty_polygon(pts, line_width=line_width, fill=context.white)

def draw_temp(context, x, y, w, h, data):
    # Temperature
    text = f'{data["temp"]}°C'
    context.image_text.write_text_box(x, y, text, w, font=context.font_normal,
        align='center', color=context.black)

    # Wind chill
    text_dim = context.draw.textsize(text, context.font_normal)
    text2 = f'gevoel {data["gtemp"]}'
    context.image_text.write_text_box(x, y+text_dim[1]+4, text2, w, font=context.font_small,
        align='center', color=context.black)

def draw_atmos(context, x, y, w, h, data):
    lv = data["lv"]
    luchtd = round(float(data["luchtd"]))
    text = f'{lv}%\n{luchtd} hPa'
    context.draw.text((x, y), text, font=context.font_small, fill=context.black)

def draw_forecast(context, x, y, w, h, data):
    text = f'Verw: {data["verw"]}'
    if data["alarm"] == "1":
        text += f' | {data["alarmtxt"]}'
    context.image_text.write_text_box(x, y, text, box_width=w, \
        font=context.font_small, color=context.black)

def draw_warning_symbol(context, x, y, r, line_width):
    x += r
    y += r
    # Triangle
    pts = [
        (x + 0.0 * r, y - 0.75 * r),
        (x + 0.87 * r, y + 0.75 * r),
        (x - 0.87 * r, y + 0.75 * r)]
    context.draw_pretty_polygon(pts, line_width=line_width, fill=context.black)
    # Exclamation mark
    pts = [(x, y - 0.3 * r), (x, y + 0.3 * r)]
    context.draw_pretty_polygon(pts, line_width=line_width, fill=context.white, outline=context.white)
    context.draw_circle((x, y + 0.6 * r), line_width/2, fill=context.white)

def draw_forecast_table(context, x, y, column_width, row_height, data):
    draw = context.draw
    font = context.font_small
    h = 5 * row_height
    now = datetime.now()
    
    # Row headers
    for i, text in enumerate(["", "Verw", "Temp", "Wind", "Zon/reg"]):
        context.image_text.write_text_box(x, y + i * row_height, text,
            box_width=column_width - 10, align='right', font=context.font_small,
            color=context.black)

    # To keep things clean
    def draw_cell(x, y, text, font=context.font_small):
        context.image_text.write_text_box(x, y, text, box_width=column_width,
            align='center', font=font, color=context.black)

    # Columns per day
    for i in range(3):
        line_x = x + (i+1) * column_width
        draw.line([(line_x, y), (line_x, y+h)])
        
        day = now + timedelta(days=i)
        day_text = day.strftime('%a')
        draw_cell(x + (i+1) * column_width, y, day_text)
        
        weersplit = data[f'd{i}weer'].split('_')
        icon_text = ''.join([weather_icons[weer] for weer in weersplit])
        draw_cell(x + (i+1) * column_width, y + 1 * row_height - 10, icon_text, font=context.font_icons_small)
        
        temp_text = f"{data[f'd{i}tmax']}/{data[f'd{i}tmin']}°C"
        draw_cell(x + (i+1) * column_width, y + 2 * row_height, temp_text)
        
        wind_text = f"{data[f'd{i}windr']} {data[f'd{i}windk']}"
        draw_cell(x + (i+1) * column_width, y + 3 * row_height, wind_text)
        
        sun_rain_text = f"{data[f'd{i}zon']}/{data[f'd{i}neerslag']}%"
        draw_cell(x + (i+1) * column_width, y + 4 * row_height, sun_rain_text)
