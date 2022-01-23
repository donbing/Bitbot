from inky.auto import auto
import pathlib
from PIL import Image, ImageFont, ImageDraw
from src.log_decorator import info_log

filePath = pathlib.Path(__file__).parent.absolute()
fontPath = str(filePath)+'/resources/04B_03__.TTF'
price_font = ImageFont.truetype(fontPath, 48)
title_font = ImageFont.truetype(fontPath, 16)
medium_font = ImageFont.truetype(fontPath, 32)
tiny_font = ImageFont.truetype(fontPath, 8)

connection_error_message = """
NO INTERNET CONNECTION
----------------------------
Please check your WIFI
----------------------------
To configure WiFi access,
connect to 'RaspPiSetup' WiFi AP
then visit raspiwifisetup.com"""


class Disker:
    def __init__(self, config):
        self.WIDTH = 400
        self.HEIGHT = 300
        self.title_font = title_font
        self.price_font = price_font
        self.tiny_font = tiny_font
        self.medium_font = medium_font
        self.config = config

    @info_log
    def draw_connection_error(self):
        None

    def show(self, image):
        rotated_image = image.rotate(self.config.display_rotation())
        quatised_image = quantise_inky(rotated_image)
        self.save_image(self.config.output_file_name(), quatised_image)

    @info_log
    def save_image(self, path, image):
        image.save(path)

    def __repr__(self):
        return f'<Disk: @{(self.WIDTH, self.HEIGHT)}>'



# 🎨 create a limited pallete image for converting our chart image
def quantise_inky(display_image):
    palette_img = Image.new("P", (1, 1))
    white_black_red = (255, 255, 255, 0, 0, 0, 255, 0, 0)
    palette_img.putpalette(white_black_red + (0, 0, 0) * 252)
    return display_image.convert('RGB').quantize(palette=palette_img)


class Inker:
    def __init__(self, config):
        self.config = config
        self.display = auto()
        self.WIDTH = self.display.WIDTH
        self.HEIGHT = self.display.HEIGHT
        self.title_font = title_font
        self.price_font = price_font
        self.tiny_font = tiny_font
        self.medium_font = medium_font

    @info_log
    def draw_connection_error(self):
        img = Image.new("P", (self.WIDTH, self.HEIGHT))
        draw = ImageDraw.Draw(img)
        # 🌌 calculate space needed for message
        message_width, message_height = draw.textsize(
            connection_error_message,
            title_font)
        # 📏 where to position the message
        message_y = (self.HEIGHT - message_height) / 2
        message_x = (self.WIDTH - message_width) / 2
        # 🖊️ draw the message at position
        draw.multiline_text(
            (message_x, message_y),
            connection_error_message,
            fill=self.display.BLACK,
            font=title_font,
            align="center")
        # 📏 position  for surrounding box
        padding = 10
        x0, y0 = (message_x - padding, message_y - padding)
        x1 = message_x + message_width + padding
        y1 = message_y + message_height + padding
        # 🖊️ draw box at position
        draw.rectangle([(x0, y0), (x1, y1)], outline=self.display.RED)
        # 📺 show the image
        self.display.set_image(img)
        self.display.show()

    @info_log
    def show(self, image):
        # 🌀 rotate the image
        image_rotation = self.config.display_rotation()
        display_image = image.rotate(image_rotation)

        three_colour_screen_types = ["yellow", "red"]

        if self.display.colour in three_colour_screen_types:
            display_image = quantise_inky(display_image)

        # 📺 show the image
        self.display.set_image(display_image)
        try:
            self.display.show()
        except RuntimeError:
            # 🪳 inky 1.3.0 bug:
            # RuntimeError("Timeout waiting for busy signal to clear.")
            pass

    def __repr__(self):
        return f'<{self.display.colour} Inky: @{(self.WIDTH, self.HEIGHT)}>'
