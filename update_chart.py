import currency_chart
import io
import inky 
import pathlib
from PIL import Image, ImageFont, ImageDraw
from pprint import pprint
import random
from inky import InkyWHAT
import RPi.GPIO as GPIO
import configparser
import socket
import time

filePath = pathlib.Path(__file__).parent.absolute()

config = configparser.ConfigParser()
config.read('./config.ini')
display_config = config["display"]

inky_display = InkyWHAT(display_config["colour"])

price_font = ImageFont.truetype(str(filePath)+'/04B_03__.TTF', 48)
title_font = ImageFont.truetype(str(filePath)+'/04B_03__.TTF', 16)

def network_connected(hostname="google.com"):
    try:
        host = socket.gethostbyname(hostname)
        socket.create_connection((host, 80), 2).close()
        return True
    except:
        time.sleep(1)
    return False

# sort positions by average colour and then by random
def BestTextPositionFor(img, possibleTextPositions):
    rgb_im = img.convert('RGB')
    ordredByAveColour = sorted(title_positions, key=lambda item: (get_average_color(*item, 60, rgb_im), random.random()))
    return ordredByAveColour[-1]

# get the aaverage colour of an area of the image
def get_average_color(x, y, n, image):
    r, g, b = 0, 0, 0
    count = 0
    for s in range(x, x+(n*3)+1):
        for t in range(y, y+n+1):
            pixlr, pixlg, pixlb = image.getpixel((s, t))
            r += pixlr
            g += pixlg
            b += pixlb
            count += 1
    return ((r/count), (g/count), (b/count))

# message to tell you that there's no internet
def draw_connection_error():
    connection_error_message = """ 
NO INTERNET LINK
-----------
Please check your connection
----------------------------
Connect to the RaspPiSetup WiFi 
Then visit raspiwifisetup.com"""
    img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
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
    inky_display.set_image(img)
    inky_display.show()
    
# wait for network connection
def wait_for_internet_connection():
    connection_error_shown = False
    while network_connected() == False:
    # draw error message if not already drawn
        if connection_error_shown == False:
            connection_error_shown = True
            draw_connection_error()
        time.sleep(10)

# check internet connection
print('await network')
wait_for_internet_connection()

print('starting..')
# fetch the chart data
chartdata = currency_chart.chart_data(config)

with io.BytesIO() as file_stream:
    print('Formatting image for display')

    # write mathplot fig to stream and open as a PIL image
    chartdata.write_to_stream(file_stream)
    file_stream.seek(0)
    plot_image = Image.open(file_stream)
    
    # find some empty graph space to place our text
    title_positions = [(40, 20), (40, 220), (210, 20), (210, 220), (125,20), (125,220)]
    selectedArea = BestTextPositionFor(plot_image, title_positions)
    
    # write our text to the image
    draw_plot_image = ImageDraw.Draw(plot_image)

    # instrument / time text
    title = config["currency"]["instrument"] + ' (' + chartdata.candle_width + ') '
    draw_plot_image.text(selectedArea, title, inky_display.BLACK, title_font)

    # % change text
    title_width, title_height = draw_plot_image.textsize(title, title_font)
    change = ((chartdata.last_close() - chartdata.start_price()) / chartdata.last_close())*100
    change_colour = (inky_display.RED if change < 0 else inky_display.BLACK)
    draw_plot_image.text((selectedArea[0]+title_width, selectedArea[1]), '{:+.2f}'.format(change) + '%', change_colour, title_font)
    
    # current price text
    price = '{:,.0f}'.format(chartdata.last_close())
    price_width, price_height = draw_plot_image.textsize(price, price_font)
    draw_plot_image.text((selectedArea[0], selectedArea[1]+11), price, inky_display.RED, price_font)

    # select some random comment depending on price action
    if random.random() < 0.5:
        if chartdata.start_price() < chartdata.last_close():
            messages=config.get('comments', 'up').split(',')
        else:
            messages=config.get('comments', 'down').split(',')
        draw_plot_image.text((selectedArea[0], selectedArea[1]+48), random.choice(messages), inky_display.BLACK, title_font)
   
    draw_plot_image.rectangle([(0, 0), (inky_display.WIDTH -1, inky_display.HEIGHT-1)], outline=inky_display.RED)
    print("displaying image")

    # create a limited pallete image for converting our chart image to.
    palette_img = Image.new("P", (1, 1))
    palette_img.putpalette((255, 255, 255, 0, 0, 0, 255, 0, 0) + (0, 0, 0) * 252)

    # rotate the image and set 3 colour palettep
    image_rotation = display_config.getint("rotation")
    display_image = plot_image.rotate(image_rotation).convert('RGB').quantize(palette=palette_img)
    
    # create the display and show the image
    inky_display.set_image(display_image) 
    inky_display.show()
    # display_image.save('last_display.png')