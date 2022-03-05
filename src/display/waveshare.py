import threading
from . import DisplayBase
import time
from PIL import ImageOps


# 🌊 supports waveshare EPDs
class Waver(DisplayBase):
    def __init__(self, device_name, config):
        device_class = self.load_device_class(device_name)
        self.display = device_class()
        self.device_name = device_name
        self.lock = threading.Lock()
        self.config = config
        self.WIDTH = self.display.width
        self.HEIGHT = self.display.height

    def load_device_class(self, device_name):
        waveshare_module = __import__('waveshare_epd.' + device_name)
        device_class = getattr(waveshare_module, device_name).EPD
        return device_class

    def size(self):
        return (self.WIDTH, self.HEIGHT)

    # 📺 show the image
    def show(self, image):
        image = image.rotate(self.config.display_rotation())
        image = image.convert('P')

        # 🖼️ crop and rescale image if needed
        if image.size != self.size():
            image = ImageOps.fit(image, self.size(), centering=(0.5, 0.5))

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
