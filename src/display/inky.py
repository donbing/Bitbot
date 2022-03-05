from . import quantise_image, white_black_red, DisplayBase
import threading
from ..configuration.log_decorator import info_log
from inky.auto import auto


# 🦑 supports Pimoroni Inky EPDs
class Inker(DisplayBase):
    def __init__(self, device_name, config):
        self.device_name = device_name
        self.lock = threading.Lock()
        self.config = config
        self.display = auto()

    def _size(self):
        return self.display.resolution

    @info_log
    def show(self, image):
        # 🌀 rotate/resize the image
        image = self.apply_rotation(image)
        image = self.resize_image(image)

        # 🎨 apply colour palette
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
