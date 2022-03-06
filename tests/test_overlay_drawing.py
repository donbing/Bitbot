from PIL import ImageFont, Image, ImageDraw, ImageChops
from src.drawing.image_utils import DrawText, TextBlock
from src.configuration.bitbot_files import use_config_dir
import unittest
import os
import pathlib

curdir = pathlib.Path(__file__).parent.resolve()
files = use_config_dir(os.path.join(curdir, "../"))

transparent = (0, 0, 0, 0)
white = (255, 255, 255)
image_file_name = 'tests/images/title_block.png'


class TestTextBlocks(unittest.TestCase):
    fontPath = str(files.resource_folder) + '/04B_03__.TTF'
    title_font = ImageFont.truetype(fontPath, 16)
    price_font = ImageFont.truetype(fontPath, 32)

    def test_text_block(self):
        block = TextBlock([
            [
                DrawText('balls' + ' (' + 'arse' + ') ', self.title_font, colour=white),
                DrawText.percentage(-50, self.title_font),
            ],
            [
                DrawText("48,000", self.price_font),
            ],
        ])

        image = Image.new('RGBA', block.size(), transparent)
        draw = ImageDraw.Draw(image)

        block.draw_on(draw)

        previous_image = Image.open(image_file_name)
        diff = ImageChops.difference(image, previous_image)

        if diff.getbbox():
            diff.save('diff.png')
            assert False, "images were different, see 'diff.png'"
            # os.system(f"code 'diff.png'")

        # image.save(image_file_name)
