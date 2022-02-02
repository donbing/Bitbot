import unittest
from src.kinky import title_font
from src.intro import Intro
from os.path import join as pjoin
import pathlib
from src.configuration.bitbot_files import use_config_dir
from src.configuration.bitbot_config import load_config_ini

curdir = pathlib.Path(__file__).parent.resolve()
files = use_config_dir(pjoin(curdir, "../"))
config = load_config_ini(files)


class IntroTests(unittest.TestCase):
    display_size = (400, 300)

    def test_showing_intro_messages(self):

        int = Intro(self.display_size, title_font, config)
        int.page_duration = 1

        for idx, image in enumerate(int.play()):
            image.save(f'testimage{idx}.png')
