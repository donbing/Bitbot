from ..configuration.log_decorator import info_log
from . import DisplayBase, quantise_image, white_black_red


# 💾 saves images to disk location speficied in config
class Disker(DisplayBase):
    def __init__(self, device_name, config):
        self.device_name = device_name
        self.width, self.height = (400, 300)
        self.config = config

    def _size(self):
        return (self.width, self.height)

    @info_log
    def draw_connection_error(self):
        None

    def show(self, image):
        image = self.apply_rotation(image)
        image = quantise_image(image, white_black_red)
        self.save_image(self.config.output_file_name(), image)

    @info_log
    def save_image(self, path, image):
        image.save(path)

    def __repr__(self):
        return f'<Image to Disk: @{self.size()}>'
