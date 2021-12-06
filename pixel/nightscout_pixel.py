
import colorsys
import board
import neopixel

# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 1

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=True, pixel_order=ORDER
)

color_map = [
    (0.0, 240),
    (3.0, 240), # blue
    (4.5, 180), # cyan
    (6.0, 120), # green
    (9.0, 60), # yellow
    (11.0, 0), # red
    (13.0, -60), # magenta
    (100.0, -60)
]

def draw_ns_pixel(data):
    sgv = data["sgv"]

    # Interpolate color map
    hue = 270
    for p1, p2 in zip(color_map[:-1], color_map[1:]):
        if p1[0] <= sgv < p2[0]:
            hue = ((sgv - p1[0]) / (p2[0] - p1[0]) * (p2[1] - p1[1]) + p1[1]) % 360
            break

    # Set the pixel
    set_pixel_color(hue, 1.0, 0.3)

def set_pixel_color(hue, saturation, value):
    rgb = colorsys.hsv_to_rgb(hue / 360, saturation, value)
    pixels.fill([int(c * 255) for c in rgb])

def turn_off_pixel():
    pixels.fill([0, 0, 0])
