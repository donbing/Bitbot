from PIL import Image, ImageDraw
import time
from .image_utils import draw_centered_text
from .network_utils import wait_for_internet_connection
page1 = '''Hi, I'm your new Bitbot.

I can chart crypto and stock markets.

If you fancy a change,
I can also display pictures.
'''

page2 = '''First, I need to connect to your WiFi.

From your phone or laptop,
sign-in to the Bitbot WiFi
and follow the instructions on-screen.

Once I have internet access,
I will load the next page...
'''

page3 = '''Good job! I'm connected :D

To change my config,
visit 'http://bitbot:8080'
from any device in your network.

In 30 seconds time,
I'll show the Bitcoin chart for you
Have fun!
'''

white = (255, 255, 255)


def IntroPlayer(display):
    intro = Intro(display.size, display.title_font)
    for image in intro.play():
        display.show(image)


class Intro:
    def __init__(self, size, font):
        self.clear = Image.new("P", size, 7)
        self.display_size = size
        self.font = font
        self.centre = tuple(dim / 2 for dim in self.display_size)
        self.page_duration = 30

    def play(self):
        img = Image.new("P", self.display_size, white)
        draw = ImageDraw.Draw(img)
        draw_centered_text(draw, page1, self.font, self.display_size)
        yield img
        time.sleep(self.page_duration)
        img = Image.new("P", self.display_size, white)
        draw = ImageDraw.Draw(img)
        draw_centered_text(draw, page2, self.font, self.display_size)
        yield img
        wait_for_internet_connection(self.no_op)
        img = Image.new("P", self.display_size, white)
        draw = ImageDraw.Draw(img)
        draw_centered_text(draw, page3, self.font, self.display_size)
        yield img
        time.sleep(self.page_duration)

    def no_op(self):
        pass
