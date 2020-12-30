import os

black = 0
white = 1

def draw_wind(draw, x, y, w, h, font, data):
    text = f'{data["windr"]} {data["winds"]}'
    text_dim = draw.textsize(text, font)
    draw.text((x, y+h-text_dim[1]), text, font=font)
    draw.rectangle([x, y, x+w, y+h-text_dim[1]-4], fill=white, outline=black)

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
