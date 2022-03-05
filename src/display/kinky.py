import inspect
import time
from inky.auto import auto
import pathlib
import threading
from PIL import Image, ImageFont, ImageDraw, ImageOps
from ..configuration.log_decorator import info_log
from ..image_utils import draw_centered_text

filePath = pathlib.Path(__file__).parent.absolute()
fontPath = str(filePath)+'/resources/04B_03__.TTF'
price_font = ImageFont.truetype(fontPath, 48)
medium_font = ImageFont.truetype(fontPath, 32)
title_font = ImageFont.truetype(fontPath, 16)
tiny_font = ImageFont.truetype(fontPath, 8)

connection_message = """
NO INTERNET CONNECTION
----------------------------
Please check your WIFI
----------------------------
To configure WiFi access,
connect to 'bitbot-<nnn>' WiFi AP
and follow the instructions"""

white_black_red = (255, 255, 255, 0, 0, 0, 255, 0, 0)


# ✒️ select EPD display or file output (nice for testing)
def picker(config):
    # todo: name classes to match config values
    typeMap = {
            'disk': Disker,
            'inky': Inker,
            'waveshare': Waver
        }
    output_device = config.output_device_name()
    manufacturer, device_name, *_ = output_device.split('.') + [None]
    return typeMap[manufacturer](device_name, config)


# 🎨 create a limited pallete image for converting our image
def quantise_image(image, palette):
    palette_img = Image.new("P", (1, 1))
    palette_img.putpalette(palette + (0, 0, 0) * 252)
    return image.convert('RGB').quantize(palette=palette_img)


class Disker:
    def __init__(self, device_name, config):
        self.device_name = device_name
        self.WIDTH = 400
        self.HEIGHT = 300
        self.title_font = title_font
        self.price_font = price_font
        self.tiny_font = tiny_font
        self.medium_font = medium_font
        self.config = config

    def size(self):
        return (self.WIDTH, self.HEIGHT)

    @info_log
    def draw_connection_error(self):
        None

    def show(self, image):
        rotated_image = image.rotate(self.config.display_rotation())
        quantised_image = quantise_image(rotated_image, white_black_red)
        self.save_image(self.config.output_file_name(), quantised_image)

    @info_log
    def save_image(self, path, image):
        image.save(path)

    def __repr__(self):
        return f'<Image to Disk: @{(self.WIDTH, self.HEIGHT)}>'


class Waver:
    def __init__(self, device_name, config):
        device_class = self.load_device_class(device_name)
        self.display = device_class()
        self.device_name = device_name
        self.lock = threading.Lock()
        self.config = config
        self.WIDTH = self.display.width
        self.HEIGHT = self.display.height
        self.title_font = title_font
        self.price_font = price_font
        self.tiny_font = tiny_font
        self.medium_font = medium_font

    def load_device_class(self, device_name):
        waveshare_module = __import__('waveshare_epd.' + device_name)
        device_class = getattr(waveshare_module, device_name).EPD
        return device_class

    def size(self):
        return (self.WIDTH, self.HEIGHT)

    @info_log
    # 📺 show error image
    def draw_connection_error(self):
        img = Image.new("P", self.size())
        draw = ImageDraw.Draw(img)
        draw_centered_text(draw, connection_message, title_font, self.size(), border=True)
        self.show(img)

    # 📺 show the image
    def show(self, image):
        image = image.rotate(self.config.display_rotation())
        image = image.convert('P')

        # create a bw image frm our source
        black_image = image.copy()
        black_image.putpalette((255, 255, 255, 0, 0, 0))
        # create an image for the red colour channel
        color_image = image.copy()
        color_image.putpalette((255, 255, 255, 255, 255, 255, 0, 0, 0) + (255, 255, 255)*253)

        epd = self.display
        epd.init()
        epd.Clear()

        time.sleep(1)

        # maybe use the arg names to discern how to call 'display' :()
        # args = inspect.getfullargspec(self.display.display)
        epd.display(epd.getbuffer(black_image), epd.getbuffer(color_image))
        epd.sleep()

    def __repr__(self):
        return f'<{self.device_name}: @{(self.WIDTH, self.HEIGHT)}>'


class Inker:
    def __init__(self, device_name, config):
        self.device_name = device_name
        self.lock = threading.Lock()
        self.config = config
        self.display = auto()
        self.WIDTH, self.HEIGHT = self.display.resolution
        self.title_font = title_font
        self.price_font = price_font
        self.tiny_font = tiny_font
        self.medium_font = medium_font

    def size(self):
        return self.display.resolution

    @info_log
    def draw_connection_error(self):
        img = Image.new("P", self.size())
        draw = ImageDraw.Draw(img)
        draw_centered_text(draw, connection_message, title_font, self.size(), border=True)
        # 📺 show the image
        self.display.set_image(img)
        self.display.show()

    @info_log
    def show(self, image):
        # 🌀 rotate the image
        image_rotation = self.config.display_rotation()
        display_image = image.rotate(image_rotation)

        # 🖼️ crop and rescale image if needed
        if display_image.size != self.size():
            display_image = ImageOps.fit(
                    display_image,
                    self.size(),
                    centering=(0.5, 0.5))

        if self.display.colour in ["yellow", "red", 'black']:
            display_image = quantise_image(display_image, white_black_red)

        self.lock.acquire()
        # 📺 show the image
        self.display.set_image(display_image)
        try:
            self.display.show()
        except RuntimeError:
            # 🐞 inky 1.3.0 bug:
            # RuntimeError("Timeout waiting for busy signal to clear.")
            pass
        finally:
            self.lock.release()

    def __repr__(self):
        return f'<Inky {self.display.colour}: @{self.size()}>'
