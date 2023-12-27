from PIL import Image
import numpy as np

def draw_sunspot_image(context, x, y, w, h, data):
    if isinstance(data, np.ndarray):
        img = Image.fromarray(data)
        region = (x, y, x + w, y + h)
        context.image.paste(img, region)

def draw_sunspot_number(context, x, y, w, h, data):
    text = data["sunspot_number"]
    context.image_text.write_text_box(x, y, text, w,
        font=context.font_small, color=context.black, align='center')

def draw_kp_index(context, x, y, w, h, kp_data):
    kp_index = kp_data["kp"]
    text = f'Kp {kp_index}'
    context.image_text.write_text_box(x, y, text, w,
        font=context.font_small, color=context.black)
