from datetime import datetime

def draw_date(context, x, y):
    text = datetime.now().strftime("%A %-d %B %Y")
    context.draw.text((x, y), text, font=context.font_normal)

def draw_time(context, x_right, y, font):
    text = datetime.now().strftime("%H:%M")
    text_dim = context.draw.textsize(text, font)
    context.draw.text((x_right - text_dim[0], y), text, font=font)
