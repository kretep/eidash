from PIL import Image

def draw_sunspots(context, x, y, w, h, data):
    img = Image.fromarray(data)
    region = (x, y, x + w, y + h)
    context.image.paste(img, region)

def draw_sunspot_number(context, x, y, w, h, data):
    text = data["sunspot_number"]
    context.image_text.write_text_box(x, y, text, w,
        font=context.font_small, color=context.black, align='center')
