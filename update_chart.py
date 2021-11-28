import currency_chart
import io
from PIL import Image, ImageFont, ImageDraw
from pprint import pprint
import random
import RPi.GPIO as GPIO
import configparser
import socket
import time
import kinky

config = configparser.ConfigParser()
config.read('./config.ini')

display = kinky.inker(config)
#display = kinky.disker()

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

# wait for network connection
def wait_for_internet_connection():
    connection_error_shown = False
    while network_connected() == False:
    # draw error message if not already drawn
        if connection_error_shown == False:
            connection_error_shown = True
            display.draw_connection_error()
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
    title_positions = [(60, 5), (210, 5), (140, 5), (60, 200), (210, 200), (140, 200)] 
    selectedArea = BestTextPositionFor(plot_image, title_positions)
    
    # write our text to the image
    draw_plot_image = ImageDraw.Draw(plot_image)

    # instrument / time text
    title = config["currency"]["instrument"] + ' (' + chartdata.candle_width + ') '
    draw_plot_image.text(selectedArea, title, 'black', display.title_font)

    # % change text
    title_width, title_height = draw_plot_image.textsize(title, display.title_font)
    change = ((chartdata.last_close() - chartdata.start_price()) / chartdata.last_close())*100
    change_colour = ('red' if change < 0 else 'black')
    draw_plot_image.text((selectedArea[0]+title_width, selectedArea[1]), '{:+.2f}'.format(change) + '%', change_colour, display.title_font)
    
    # current price text
    price = '{:,.0f}'.format(chartdata.last_close())
    price_width, price_height = draw_plot_image.textsize(price, display.price_font)
    draw_plot_image.text((selectedArea[0], selectedArea[1]+11), price, 'black', display.price_font)
    
    # select some random comment depending on price action
    if random.random() < 0.5:
        direction = 'up' if chartdata.start_price() < chartdata.last_close() else 'down'
        messages=config.get('comments', direction).split(',')
        draw_plot_image.text((selectedArea[0], selectedArea[1]+52), random.choice(messages), 'red', display.title_font)
   
    draw_plot_image.rectangle([(0, 0), (display.WIDTH -1, display.HEIGHT-1)], outline='red')
    
    print("displaying image")
    display.show(plot_image) 