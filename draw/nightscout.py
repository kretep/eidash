
def draw_nightscout(context, x, y, w, h, data):
    # Main value
    main_text = f'{data["sgv"]}{data["direction"]}'
    context.draw.text((x, y), main_text, font=context.font_normal, fill=context.black)

    # Delta
    main_size = context.draw.textsize(main_text, context.font_normal)
    delta_text = f'{data["delta"]}\n[{data["minutes_ago"]}m]'
    context.draw.text((x + main_size[0], y), delta_text, font=context.font_small, fill=context.black)
