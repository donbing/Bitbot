from PIL import ImageFont, Image, ImageDraw
from src.drawing.image_utils import DrawText, TextBlock
import unittest
import os
import pathlib

# check config files
curdir = pathlib.Path(__file__).parent.resolve()
files = use_config_dir(os.path.join(curdir, "../"))

transparent = (0, 0, 0, 0)
white = (255, 255, 255)


class TestTextBlocks(unittest.TestCase):
    fontPath = str(files.resource_folder) + '/04B_03__.TTF'
    title_font = ImageFont.truetype(fontPath, 16)
    price_font = ImageFont.truetype(fontPath, 32)
    image_file_name = f'tests/images/title_block.png'

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
        image.save(image_file_name)

        diff = ImageChops.difference(image, previous_image)

        if diff.getbbox():
            diff.save('diff.png')
            assert False "images were different, see 'diff.png'"
            
        # os.system(f"code '{image_file_name}'")
