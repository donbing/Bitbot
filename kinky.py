
from inky import InkyWHAT
import pathlib
from PIL import Image, ImageFont, ImageDraw

connection_error_message = """ 
NO INTERNET LINK
----------------------------
Please check your connection
----------------------------
Connect to the RaspPiSetup WiFi 
Then visit raspiwifisetup.com"""

filePath = pathlib.Path(__file__).parent.absolute()
price_font = ImageFont.truetype(str(filePath)+'/04B_03__.TTF', 48)
title_font = ImageFont.truetype(str(filePath)+'/04B_03__.TTF', 16)

class disker:
    def __init__(self):
        self.WIDTH = 400
        self.HEIGHT = 300
        self.BLACK = 1
        self.RED = 2
        self.title_font = title_font
        self.price_font = price_font
    
    def draw_connection_error(self):
        print("no connection")
    
    def show(self, display_image):
        display_image.save('last_display.png')
thislist = []
class inker:
    def __init__(self, config):
        self.display_config = config["display"]
        self.inky_display = InkyWHAT(self.display_config["colour"])
        self.WIDTH = self.inky_display.WIDTH
        self.HEIGHT = self.inky_display.HEIGHT
        self.BLACK = self.inky_display.BLACK
        self.RED = self.inky_display.RED
        self.title_font = title_font
        self.price_font = price_font
    
    def draw_connection_error(self):
        img = Image.new("P", (display.WIDTH, display.HEIGHT))
        draw = ImageDraw.Draw(img)
        # calculate space needed for message
        message_width, message_height = draw.textsize(connection_error_message, title_font)
        # where to position the message
        message_y = (inky_display.HEIGHT - message_height) / 2
        message_x = (inky_display.WIDTH - message_width) / 2
        # draw the message at position
        draw.multiline_text((message_x, message_y), connection_error_message, fill=inky_display.BLACK, font=title_font, align="center")
        # position  for surrounding box
        padding = 10
        x0 = message_x - padding
        y0 = message_y - padding
        x1 = message_x + message_width + padding
        y1 = message_y + message_height + padding
        # draw box at position
        draw.rectangle([(x0, y0), (x1, y1)], outline=inky_display.RED)
        # show the image
        self.show(img)
    
    def show(self, image, draw_plot_image):
        # create a limited pallete image for converting our chart image to.
        palette_img = Image.new("P", (1, 1))
        palette_img.putpalette((255, 255, 255, 0, 0, 0, 255, 0, 0) + (0, 0, 0) * 252)

        # rotate the image and set 3 colour palettep
        image_rotation = self.display_config.getint("rotation")
        display_image = image.rotate(image_rotation).convert('RGB').quantize(palette=palette_img)
    
        self.inky_display.set_image(display_image) 
        self.inky_display.show()
