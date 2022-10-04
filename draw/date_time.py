from datetime import datetime

def draw_date(context, x, y):
    now = datetime.now()
    text = now.strftime("%A ").capitalize() + now.strftime("%-d %B %Y")
    context.draw.text((x, y), text, font=context.font_time)

def draw_time(context, x_right, y):
    text = datetime.now().strftime("%H:%M")
    text_dim = context.draw.textsize(text, context.font_time)
    context.draw.text((x_right - text_dim[0], y), text, font=context.font_time)
