from PIL import Image, ImageDraw, ImageFont, ImageOps
from ..configuration.log_decorator import info_log
from ..drawing.image_utils import centered_text
import pathlib
white_black_red = (255, 255, 255, 0, 0, 0, 255, 0, 0)

filePath = pathlib.Path(__file__).parent.parent.absolute()
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


# 🎨 create a limited pallete image for converting our image
def quantise_image(image, palette):
    palette_img = Image.new("P", (1, 1))
    palette_img.putpalette(palette + (0, 0, 0) * 252)
    return image.convert('RGB').quantize(palette=palette_img)


# 🔝 simple base class for all displays
class DisplayBase:
    title_font = title_font
    price_font = price_font
    tiny_font = tiny_font
    medium_font = medium_font

    def size(self):
        size = self._size()
        rotation = self.config.display_rotation()
        return size if rotation % 180 == 0 else size[::-1]

    def set_fonts(self):
        if(self.size()[0] < 300):
            self.price_font = medium_font
            self.medium_font = title_font
            self.title_font = tiny_font

    @info_log
    # 📺 show error image
    def draw_connection_error(self):
        img = Image.new("P", self.size())
        draw = ImageDraw.Draw(img)
        centered_text(draw, connection_message, title_font, self.size(), border=True)
        self.show(img)

    # 🔁 apply rotation (see size() for why this is weird)
    def apply_rotation(self, image):
        image_rotation = self.config.display_rotation()
        if(image_rotation == 180):
            return image.rotate(180)
        elif(image_rotation == 270):
            return image.rotate(180)
        else:
            return image

    @info_log
    # 🖼️ crop and rescale image if needed
    def resize_image(self, image):
        if image.size != self.size():
            return ImageOps.fit(image, self.size(), centering=(0.5, 0.5))
        return image
