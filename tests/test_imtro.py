import unittest
from src.kinky import title_font
from src.intro import Intro


class IntroTests(unittest.TestCase):
    display_size = (400, 300)

    def test_showing_intro_messages(self):

        int = Intro(self.display_size, title_font)
        int.page_duration = 1

        for idx, image in enumerate(int.play()):
            image.save(f'testimage{idx}.png')
