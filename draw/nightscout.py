
def draw_nightscout(context, x, y, w, h, data):
    main_text = f'{data["sgv"]}{data["direction"]}'
    delta_text = f'{data["delta"]}\n[{data["minutes_ago"]}m]'

    # Determine text size
    main_size = context.draw.textsize(main_text, context.font_normal)
    delta_size = context.draw.textsize(delta_text, context.font_small)
    x_main = x + (w - main_size[0] - delta_size[0]) / 2
    x_delta = x_main + main_size[0]

    # Main value
    context.draw.text((x_main, y), main_text, font=context.font_normal, fill=context.black)

    # Delta
    context.draw.text((x_delta, y), delta_text, font=context.font_small, fill=context.black)
