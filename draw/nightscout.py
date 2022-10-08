
def draw_nightscout(context, x, y, w, h, data):
    minutes_ago = data["minutes_ago"]
    minutes_ago_text = str(minutes_ago) if minutes_ago >= 0 else "?"
    main_text = f'{data["sgv"]}{data["direction"]}'
    delta_text = f'{data["delta"]}\n[{minutes_ago_text}m]'

    # Determine text size
    main_size = context.draw.textsize(main_text, context.font_normal)
    delta_size = context.draw.textsize(delta_text, context.font_small)
    main_x = x + (w - main_size[0] - delta_size[0]) / 2
    delta_x = main_x + main_size[0]

    # Main value
    context.draw.text((main_x, y), main_text, font=context.font_normal, fill=context.black)

    # Strikethrough for old data
    if minutes_ago > 8:
        line_y = y + main_size[1] / 2 + 2
        context.draw.line([(main_x, line_y), (main_x + main_size[0], line_y)], width=3, fill=context.black)

    # Delta
    context.draw.text((delta_x, y), delta_text, font=context.font_small, fill=context.black)
