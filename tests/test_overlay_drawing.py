from PIL import ImageFont, Image, ImageDraw, ImageChops
from src.drawing.image_utils.DrawText import DrawText
from src.drawing.image_utils.TextBlock import TextBlock
from src.drawing.image_utils.CenteredText import centered_text
from src.configuration.bitbot_files import use_config_dir
import unittest
import os
import pathlib

current_directory = pathlib.Path(__file__).parent.resolve()
files = use_config_dir(os.path.join(current_directory, "../"))

transparent = (0, 0, 0, 0)
white = (255, 255, 255)


class TestTextBlocks(unittest.TestCase):
    fontPath = str(files.resource_folder) + '/04B_03__.TTF'
    title_font = ImageFont.truetype(fontPath, 16)
    price_font = ImageFont.truetype(fontPath, 32)

    def test_text_block(self):
        image_file_name = 'tests/images/title_block.png'
        block = TextBlock([
            [
                DrawText('GBP' + ' (' + 'Sterling' + ') ', self.title_font, colour=white),
                DrawText.percentage(-50, self.title_font),
            ],
            [
                DrawText("48,000", self.price_font),
            ],
        ])

        image = Image.new('RGBA', block.size(), transparent)
        image_drawing = ImageDraw.Draw(image)
        block.draw_on(image_drawing)

        previous_image = Image.open(image_file_name) if os.path.isfile(image_file_name) else None
        if previous_image is None:
            assert False, f"New image result, re-run the test to accept: '{image_file_name}'"

        image.save(image_file_name)
        diff = ImageChops.difference(image, previous_image)
        if diff.getbbox():
            file_name = f'tests/images/overlay_diff.png'
            diff.save(file_name)
            assert False, f"images were different, see '{file_name}'"
            # os.system(f"code 'diff.png'")

            
    def test_centered(self):
        image_file_name = 'tests/images/test_centered.png'
        image = Image.new("RGBA", (400, 300), transparent)
        draw = ImageDraw.Draw(image)
        centered_text(draw, "test", self.price_font, image.size, 'centre', border=True)

        previous_image = Image.open(image_file_name) if os.path.isfile(image_file_name) else None
        if previous_image is None:
            assert False, f"New image result, re-run the test to accept: '{image_file_name}'"

        image.save(image_file_name)
        diff = ImageChops.difference(image, previous_image)
        if diff.getbbox():
            file_name = f'tests/images/test_centered_diff.png'
            diff.save(file_name)
            assert False, f"images were different, see '{image_file_name}'"
            # os.system(f"code '{image_file_name}'")
