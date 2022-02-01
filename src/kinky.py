from inky.auto import auto
import pathlib
import threading
from PIL import Image, ImageFont, ImageDraw, ImageOps
from .configuration.log_decorator import info_log
from .image_utils import draw_centered_text

filePath = pathlib.Path(__file__).parent.absolute()
fontPath = str(filePath)+'/resources/04B_03__.TTF'
price_font = ImageFont.truetype(fontPath, 48)
title_font = ImageFont.truetype(fontPath, 16)
medium_font = ImageFont.truetype(fontPath, 32)
tiny_font = ImageFont.truetype(fontPath, 8)

connection_message = """
NO INTERNET CONNECTION
----------------------------
Please check your WIFI
----------------------------
To configure WiFi access,
connect to 'bitbot-<nnn>' WiFi AP
and follow the instructions"""


# ✒️ select inky display or file output (nice for testing)
def picker(config):
    if config.use_inky():
        return Inker(config)
    else:
        return Disker(config)


class Disker:
    def __init__(self, config):
        self.WIDTH = 400
        self.HEIGHT = 300
        self.title_font = title_font
        self.price_font = price_font
        self.tiny_font = tiny_font
        self.medium_font = medium_font
        self.config = config
        self.size = (self.WIDTH, self.HEIGHT)

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
        return f'<Image to Disk: @{(self.WIDTH, self.HEIGHT)}>'


# 🎨 create a limited pallete image for converting our chart image
def quantise_inky(display_image):
    palette_img = Image.new("P", (1, 1))
    white_black_red = (255, 255, 255, 0, 0, 0, 255, 0, 0)
    palette_img.putpalette(white_black_red + (0, 0, 0) * 252)
    return display_image.convert('RGB').quantize(palette=palette_img)


class Inker:
    def __init__(self, config):
        self.lock = threading.Lock()
        self.config = config
        self.display = auto()
        self.WIDTH = self.display.WIDTH
        self.HEIGHT = self.display.HEIGHT
        self.title_font = title_font
        self.price_font = price_font
        self.tiny_font = tiny_font
        self.medium_font = medium_font
        self.size = (self.WIDTH, self.HEIGHT)

    @info_log
    def draw_connection_error(self):
        img = Image.new("P", self.size)
        draw = ImageDraw.Draw(img)
        draw_centered_text(draw, connection_message, title_font, self.size)
        # 📺 show the image
        self.display.set_image(img)
        self.display.show()

    @info_log
    def show(self, image):
        # 🌀 rotate the image
        image_rotation = self.config.display_rotation()
        display_image = image.rotate(image_rotation)

        three_colour_screen_types = ["yellow", "red"]

        # 🖼️ crop and rescale image if it doesnt match the display dims
        if display_image.size != self.size:
            display_image = ImageOps.fit(
                    display_image,
                    self.size,
                    centering=(0.5, 0.5))

        if self.display.colour in three_colour_screen_types:
            display_image = quantise_inky(display_image)

        self.lock.acquire()
        # 📺 show the image
        self.display.set_image(display_image)
        try:
            self.display.show()
        except RuntimeError:
            # 🪳 inky 1.3.0 bug:
            # RuntimeError("Timeout waiting for busy signal to clear.")
            pass
        finally:
            self.lock.release()

    def __repr__(self):
        return f'<{self.display.colour} Inky: @{self.size}>'
