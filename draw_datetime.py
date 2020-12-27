from datetime import datetime

def draw_date(draw, x, y, font):
    text = datetime.now().strftime("%A %-d %B %Y")
    draw.text((x, y), text, font=font)

def draw_time(draw, x_right, y, font):
    text = datetime.now().strftime("%H:%M")
    text_dim = draw.textsize(text, font)
    draw.text((x_right - text_dim[0], y), text, font=font)
