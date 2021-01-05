from PIL import Image

def draw_sunspots(image, x, y, w, h, data):
    img = Image.fromarray(data)
    region = (x, y, x + w, y + h)
    image.paste(img, region)
