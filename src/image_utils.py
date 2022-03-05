from PIL import Image, ImageDraw

padding = 10
transparent = (0, 0, 0, 0)


# 🏳️ select image area with the most white pixels
def least_intrusive_position(img, block):
    possiblePositions = possible_block_positions(img, block)

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

    rgb_im = img.convert('RGB')
    height_of_section = block.height
    width_of_section = block.width
    ordredByAveColour = sorted(
        possiblePositions,
        key=lambda item: (
            count_white_pixels(*item, height_of_section, width_of_section, rgb_im),
            item[0])
        )

    return ordredByAveColour[-1]


def possible_block_positions(image, text_block):
    width, height = image.size
    left_pad = 60
    top_pad = 6
    x_range = range(left_pad, width - text_block.width, 10)
    y_range = [top_pad, height // 2, height - text_block.height]
    return flatten(
        map(lambda y: map(lambda x: (x, y), x_range), y_range)
    )


def flatten(t):
    return [item for sublist in t for item in sublist]


class DrawText:
    def width(text):
        return text.size[0]

    def height(text):
        return text.size[1]

    def percentage(percentage, font):
        text_color = 'red' if percentage < 0 else 'black'
        return DrawText('{:+.2f}'.format(percentage) + '%', font, text_color)

    def __init__(self, text, font, colour='black'):
        self.text = text
        self.font = font
        self.colour = colour
        self.size = font.getsize(text)


class TextBlock:
    def __init__(self, texts):
        self.texts = texts
        self.width = self.longest_line(texts)
        self.height = self.total_height(texts)

    def total_height(self, texts):
        return sum(map(lambda row: max(map(DrawText.height, row)), texts))

    def longest_line(self, texts):
        return max(map(lambda row: sum(map(DrawText.width, row)), texts))

    def size(self):
        return (self.width, self.height)

    def draw_on(self, draw, pos):
        last_y_pos = pos[1]
        for row in self.texts:
            self.draw_text_row(draw, pos, last_y_pos, row)
            last_y_pos += max(map(DrawText.height, row))

    def draw_text_row(self, draw, pos, y_pos, row):
        last_x_pos = pos[0]
        for text in row:
            draw.text((last_x_pos, y_pos), text.text, text.colour, text.font)
            last_x_pos += text.size[0]


def rotated_center_right_text(draw_on, title, font):
    text_width, text_height = draw_on.textsize(title, font)
    text_image = Image.new('RGBA', (text_width, text_height), transparent)
    text_image_draw = ImageDraw.Draw(text_image)
    text_image_draw.text((0, 0), title, 'black', font)
    rotated_text = text_image.rotate(270, expand=True)

    display_width, display_height = draw_on.im.size
    title_bottom_left = display_width - text_height - 2
    vertical_center = int((display_height - text_width) / 2)
    title_paste_pos = (title_bottom_left, vertical_center)
    draw_on._image.paste(rotated_text, title_paste_pos, rotated_text)


def top_right_text(draw, text, font):
    text_width, _ = draw.textsize(text, font)
    display_width, _ = draw.im.size
    text_pos = (display_width - text_width, 0)
    draw.text(text_pos, text, 'red', font)


def bottom_right_text(draw, text, font):
    text_width, text_height = draw.textsize(text, font)
    display_width, display_height = draw.im.size
    text_pos = (display_width - text_width, display_height - text_height)
    draw.text(text_pos, text, 'black', font)


def bottom_left_text(draw, text, font):
    _, text_height = draw.textsize(text, font)
    _, display_height = draw.im.size
    text_pos = (0, display_height - text_height)
    draw.text(text_pos, text, 'black', font)


def border(draw, border_type):
    display_width, display_height = draw.im.size
    rect_pos = [(0, 0), (display_width - 1, display_height - 1)]
    draw.rectangle(rect_pos, outline=border_type)


def draw_centered_text(draw, text, font, size, pos='centre', border=False):
    # 🌌 calculate space needed for message
    message_size = draw.textsize(text, font)

    # 📏 where to position the message
    if pos == 'centre':
        message_x, message_y = center_aligned(size,  message_size)
    elif pos == 'topright':
        message_x, message_y = top_right_aligned(size,  message_size)
    elif pos == 'topleft':
        message_x, message_y = top_left_aligned()

    # 🖊️ draw the message at position
    draw.multiline_text(
        (message_x, message_y),
        text,
        fill='black',
        font=font,
        align="left")

    if border:
        # 📏 position  for surrounding box
        x0, y0 = (message_x - padding, message_y - padding)
        x1 = message_x + message_size[0] + padding
        y1 = message_y + message_size[1] + padding
        # 🖊️ draw box at position
        draw.rectangle([(x0, y0), (x1, y1)], outline='red')


def top_right_aligned(display_size, message_size):
    return (display_size[0] - message_size[0] - padding - 1, padding)


def top_left_aligned():
    return (0 + padding + 1, 0 + padding + 1)


def center_aligned(display_size, message_size):
    message_y = (display_size[1] - message_size[1]) / 2
    message_x = (display_size[0] - message_size[0]) / 2
    return (message_y, message_x)
