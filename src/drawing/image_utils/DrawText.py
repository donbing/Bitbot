from src.drawing.price_humaniser import format_title_price
import random


class DrawText:
    @staticmethod
    def width(text): return text.size[0]

    @staticmethod
    def height(text): return text.size[1]

    # 🔀 coloured percentage change text
    @staticmethod
    def percentage(percentage, font):
        text_color = 'red' if percentage < 0 else 'black'
        return DrawText('{:+.2f}'.format(percentage) + '%', font, text_color)

    # 🏷️ human-readable price text
    @staticmethod
    def humanised_price(price, font, prefix=""):
        return DrawText(prefix + format_title_price(price), font)

    @staticmethod
    def pip_calc(open, close, font, prefix=""):
        if str(open).index('.') >= 3:  # JPY pair
            multiplier = 0.01
        else:
            multiplier = 0.0001

        pips = round((close - open) / multiplier)
        return DrawText(prefix + '({:+})'.format(int(pips)), font)

    # 🏷️ number text
    @staticmethod
    def number(value, font, colour='black'):
        return DrawText("{:+.2f}".format(value), font, colour)

    # 🏷️ number text
    @staticmethod
    def number_6sf(value, font):
        return DrawText("{:.5g}".format(value), font, 'black')

    # 🏷️ any text
    @staticmethod
    def draw_string(value, font):
        return DrawText(value, font, 'black')

    # 🎲 randomly selected up/down comment
    @staticmethod
    def random_from_bool(options, up_or_down, font):
        direction = 'up' if up_or_down else 'down'
        comments = random.choice(options[direction].split(','))
        return DrawText(comments, font, 'red')

    # empty
    @staticmethod
    def empty(font):
        return DrawText("", font, 'red')

    def __init__(self, text, font, colour='black', align=None):
        self.text = text
        self.font = font
        self.colour = colour
        self.size = font.getbbox(text)[-2:]
        self.align = align

    def draw_on(self, draw, pos=(0, 0)):
        pos = self.align(draw.im, self.size) if self.align else pos
        draw.text(pos, self.text, self.colour, self.font)