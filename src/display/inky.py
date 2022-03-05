from . import quantise_image, white_black_red, DisplayBase
import threading
from ..configuration.log_decorator import info_log
from inky.auto import auto
from PIL import ImageOps


# 🦑 supports Pimoroni Inky EPDs
class Inker(DisplayBase):
    def __init__(self, device_name, config):
        self.device_name = device_name
        self.lock = threading.Lock()
        self.config = config
        self.display = auto()

    def size(self):
        return self.display.resolution

    @info_log
    def show(self, image):
        # 🌀 rotate the image
        image_rotation = self.config.display_rotation()
        image = image.rotate(image_rotation)

        # 🖼️ crop and rescale image if needed
        if image.size != self.size():
            image = ImageOps.fit(image, self.size(), centering=(0.5, 0.5))

        if self.display.colour in ["yellow", "red", 'black']:
            image = quantise_image(image, white_black_red)

        self.lock.acquire()
        # 📺 show the image
        self.display.set_image(image)
        try:
            self.display.show()
        finally:
            self.lock.release()

    def __repr__(self):
        return f'<Inky {self.display.colour}: @{self.size()}>'
