from PIL import Image, ImageDraw
from ..drawing.image_utils.CenteredText import centered_text
from ..configuration.network_utils import wait_for_internet_connection
import json
import requests

page1 = '''
Hi, 
    I will count your youtube subscribers
'''
channel_id="UCAotflAHrgfuhK9Rw-C_-Ug"
your_key="AIzaSyCFJ6-vHN9KgOE3a6mjdqBcG-pYlwcRGj4"

url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={your_key}"
transparent = (255, 0, 0, 0)

class YouTubeSubscriberCount:
    def __init__(self, size, font, config):
        self.display_size = size
        self.font = font
        self.centre = tuple(dim / 2 for dim in self.display_size.size)

    def play(self):
        http_response = requests.get(url)
        response_json = json.loads(http_response.text)
        text_to_draw = "Subscribers" + response_json['items'][0]['statistics']['subscriberCount']
        img = Image.new("RGBA", self.display_size.size, transparent)
        draw = ImageDraw.Draw(img)
        centered_text(draw, text_to_draw, self.font, self.display_size, 'centre')
        return img

    def no_op(self):
        pass
