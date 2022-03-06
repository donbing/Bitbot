from PIL import Image, ImageDraw
from src.drawing.price_humaniser import format_title_price
import random

padding = 0
transparent = (0, 0, 0, 0)


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
    def humanised_price(price, font):
        return DrawText(format_title_price(price), font)

    # 🏷️ number text
    @staticmethod
    def number(value, font):
        return DrawText("{:,}".format(value), font, 'black')

    # 🎲 randomly selected up/down comment
    @staticmethod
    def random_from_bool(options, up_or_down, font):
        direction = 'up' if up_or_down else 'down'
        comments = random.choice(options[direction].split(','))
        return DrawText(comments, font, 'red')

    def __init__(self, text, font, colour='black', align=None):
        self.text = text
        self.font = font
        self.colour = colour
        self.size = font.getsize(text)
        self.align = align

    def draw_on(self, draw, pos=(0, 0)):
        pos = self.align(draw.im, self.size) if self.align else pos
        draw.text(pos, self.text, self.colour, self.font)


class TextBlock:
    def __init__(self, texts, align=None):
        self.texts = texts
        self.width = self.longest_line(texts)
        self.height = self.total_height(texts)
        self.align = align

    def total_height(self, texts):
        return sum(map(lambda row: max(map(DrawText.height, row)), texts))

    def longest_line(self, texts):
        return max(map(lambda row: sum(map(DrawText.width, row)), texts))

    def size(self):
        return (self.width, self.height)

    def draw_on(self, draw, pos=(0, 0)):
        pos = self.align(draw.im, self.size()) if self.align else pos
        last_y_pos = pos[1]
        for row in self.texts:
            self.draw_text_row(draw, pos[0], last_y_pos, row)
            last_y_pos += max(map(DrawText.height, row))

    def draw_text_row(self, draw, x_pos, y_pos, row):
        for text in row:
            text.draw_on(draw, (x_pos, y_pos))
            x_pos += DrawText.width(text)


class Border:
    def __init__(self, border_type):
        self.border_type = border_type

    def draw_on(self, draw, pos=(0, 0)):
        if self.border_type != 'none':
            draw.rectangle(Border.border_rect(draw), outline=self.border_type)

    def border_rect(draw):
        return [(0, 0), (draw.im.size[0] - 1, draw.im.size[1] - 1)]


class RotatedTextBlock:
    def __init__(self, text, font):
        self.text = text
        self.font = font

    def size(self):
        return self.font.get_size(self.text)

    def draw_on(self, draw, pos=(0, 0)):
        text_width, text_height = draw.textsize(self.text, self.font)
        text_image = Image.new('RGBA', (text_width, text_height), transparent)
        text_image_draw = ImageDraw.Draw(text_image)
        text_image_draw.text((0, 0), self.text, 'black', self.font)
        rotated_text = text_image.rotate(270, expand=True)

        display_width, display_height = draw.im.size
        title_bottom_left = display_width - text_height - 2
        vertical_center = int((display_height - text_width) / 2)
        title_paste_pos = (title_bottom_left, vertical_center)
        draw._image.paste(rotated_text, title_paste_pos, rotated_text)


def centered_text(draw, text, font, container_size, pos='centre', border=False):
    # 🌌 calculate space needed for message
    message_size = draw.textsize(text, font)
    # 📏 where to position the message
    if pos == 'centre':
        message_x, message_y = Align.Centre(container_size, message_size)
    elif pos == 'topright':
        message_x, message_y = Align.TopRight(container_size, message_size)
    elif pos == 'topleft':
        message_x, message_y = Align.TopLeft(container_size, message_size)
    # 🖊️ draw the message at position
    draw.multiline_text(
        (message_x, message_y),
        text,
        fill='black',
        font=font,
        align="left")
    # 📏 measure border box
    if border:
        x0, y0 = (message_x - padding, message_y - padding)
        x1 = message_x + message_size[0] + padding
        y1 = message_y + message_size[1] + padding
        # 🖊️ draw box at position
        draw.rectangle([(x0, y0), (x1, y1)], outline='red')


class Align:
    def TopRight(display, message_size):
        return (display.size[0] - message_size[0] - padding - 1, padding)

    def BottomRight(display, message_size):
        return (display.size[0] - message_size[0], display.size[1] - message_size[1])

    def BottomLeft(display, message_size):
        return (0, display.size[1] - message_size[1])

    def TopLeft(display, message_size):
        return (0 + padding + 1, 0 + padding + 1)

    def Centre(display, message_size):
        message_y = (display.size[1] - message_size[1]) / 2
        message_x = (display.size[0] - message_size[0]) / 2
        return (message_y, message_x)

    # 🏳️ select image area with the most white pixels
    def LeastIntrusive(display, block):
        possiblePositions = Align.possible_block_positions(display, block)
        block_width, block_height = block

        # 🔢 count the white pixels in an area of the image
        def count_white_pixels(x, y, height, width, image):
            count = 0
            x_range = range(x, x + width)
            y_range = range(y, y + height)
            for x in x_range:
                for y in y_range:
                    pix = image.getpixel((x, y))
                    count += 1 if pix == (255, 255, 255) else 0
            return count

        rgb_im = display.convert('RGB')
        ordredByAveColour = sorted(
            possiblePositions,
            key=lambda item: (
                count_white_pixels(*item, block_height, block_width, rgb_im),
                item[0])
            )
        if len(ordredByAveColour) > 0:
            return ordredByAveColour[-1]
        return (0, 0)

    def possible_block_positions(image, text_size):
        image_width, image_height = image.size
        text_width, text_height = text_size
        left_pad, top_pad = (0, 0)

        x_range = range(left_pad, image_width - text_width, 10)
        y_range = [top_pad, image_height // 2, image_height - text_height]
        return Align.flatten(
            map(lambda y: map(lambda x: (x, y), x_range), y_range)
        )

    def flatten(t):
        return [item for sublist in t for item in sublist]
