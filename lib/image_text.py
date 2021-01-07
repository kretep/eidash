#!/usr/bin/env python
# coding: utf-8

# Copyright 2011 Álvaro Justen [alvarojusten at gmail dot com]
# License: GPL <http://www.gnu.org/copyleft/gpl.html>

# Adapted from: https://gist.github.com/turicas/1455973

from PIL import ImageFont


class ImageText(object):
    def __init__(self, image, draw):
        self.image = image
        self.draw = draw
        self.size = self.image.size

    def get_font_size(self, text, font, max_width=None, max_height=None):
        if max_width is None and max_height is None:
            raise ValueError('You need to pass max_width or max_height')
        font_size = 1
        text_size = self.get_text_size(font, font_size, text)
        if (max_width is not None and text_size[0] > max_width) or \
           (max_height is not None and text_size[1] > max_height):
            raise ValueError("Text can't be filled in only (%dpx, %dpx)" % \
                    text_size)
        while True:
            if (max_width is not None and text_size[0] >= max_width) or \
               (max_height is not None and text_size[1] >= max_height):
                return font_size - 1
            font_size += 1
            text_size = self.get_text_size(font, font_size, text)

    def write_text(self, xy, text, font_filename, font_size=11,
                   color=(0, 0, 0), max_width=None, max_height=None):
        (x, y) = xy
        if font_size == 'fill' and \
           (max_width is not None or max_height is not None):
            font_size = self.get_font_size(text, font_filename, max_width,
                                           max_height)
        text_size = self.get_text_size(font_filename, font_size, text)
        font = ImageFont.truetype(font_filename, font_size)
        if x == 'center':
            x = (self.size[0] - text_size[0]) / 2
        if y == 'center':
            y = (self.size[1] - text_size[1]) / 2
        self.draw.text((x, y), text, font=font, fill=color)
        return text_size

    def get_text_size(self, font_filename, font_size, text):
        font = ImageFont.truetype(font_filename, font_size)
        return font.getsize(text)

    def write_text_box(self, x, y, text, box_width, font,
                       color=(0, 0, 0), align='left',
                       justify_last_line=False):
        text_height = 0
        lines = []
        line = []
        words = text.split()
        for word in words:
            new_line = ' '.join(line + [word])
            size = font.getsize(new_line)
            text_height = size[1]
            if size[0] <= box_width:
                line.append(word)
            else:
                lines.append(line)
                line = [word]
        if line:
            lines.append(line)
        lines = [' '.join(line) for line in lines if line]
        line_y = y
        for index, line in enumerate(lines):
            if align == 'left':
                self.draw.text((x, line_y), line, font=font, fill=color)
            elif align == 'right':
                total_size = font.getsize(line)
                x_left = x + box_width - total_size[0]
                self.draw.text((x_left, line_y), line, font=font, fill=color)
            elif align == 'center':
                total_size = font.getsize(line)
                x_left = int(x + ((box_width - total_size[0]) / 2))
                self.draw.text((x_left, line_y), line, font=font, fill=color)
            elif align == 'justify':
                words = line.split()
                if (index == len(lines) - 1 and not justify_last_line) or \
                    len(words) == 1:
                    self.draw.text((x, line_y), line, font=font, fill=color)
                    continue
                line_without_spaces = ''.join(words)
                total_size = font.getsize(line_without_spaces)
                space_width = (box_width - total_size[0]) / (len(words) - 1.0)
                word_x = x
                for word in words[:-1]:
                    self.draw.text((word_x, line_y), word, font=font, fill=color)
                    word_size = font.getsize(word)
                    word_x += word_size[0] + space_width
                last_word_size = font.getsize(words[-1])
                last_word_x = x + box_width - last_word_size[0]
                self.draw.text((last_word_x, line_y), words[-1], font=font, fill=color)
            line_y += text_height
        return (box_width, line_y - y)
