
black = 0
white = 1

def draw_nightscout(draw, x, y, w, h, font, font2, data):
    # Main value
    main_text = f'{data["sgv"]}{data["direction"]}'
    draw.text((x, y), main_text, font=font, fill=black)

    # Delta
    main_size = draw.textsize(main_text, font)
    delta_text = f'{data["delta"]}\n[{data["minutes_ago"]}m]'
    draw.text((x + main_size[0], y), delta_text, font=font2, fill=black)
