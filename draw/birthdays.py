from datetime import datetime

def draw_birthdays(context, x, y, data):
    age_text = lambda year: f' ({(datetime.now().year - year)})' if year != None else ""
    names = [f'{birthday["name"]}{age_text(birthday["year"])}' for birthday in data]
    if len(names) > 0:
        text = 'Jarig: ' + ', '.join(names)
        context.draw.text((x, y), text, font=context.font_small)
