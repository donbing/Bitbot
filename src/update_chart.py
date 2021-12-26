from src import currency_chart
from src import kinky
from PIL import Image, ImageFont, ImageDraw
import io
import random
import RPi.GPIO as GPIO
import socket
import time
import logging

def network_connected(hostname="google.com"):
    try:
        host = socket.gethostbyname(hostname)
        socket.create_connection((host, 80), 2).close()
        return True
    except:
        time.sleep(1)
    return False

# sort positions by average colour and then by random
def least_intrusive_position(img, possibleTextPositions):
    rgb_im = img.convert('RGB')
    height_of_section = 60
    ordredByAveColour = sorted(possibleTextPositions, key=lambda item: (count_white_pixels(*item, height_of_section, rgb_im), item[0]))
    return ordredByAveColour[-1]

# count the white pixels in an area of the image
def count_white_pixels(x, y, n, image):
    count = 0
    for s in range(x, x+(n*3)+1):
        for t in range(y, y+n+1):
            pix = image.getpixel((s, t))
            count += 1 if pix == (255,255,255) else 0
    return count

# wait for network connection
def wait_for_internet_connection(display):
    connection_error_shown = False
    while network_connected() == False:
        # draw error message if not already drawn
        if connection_error_shown == False:
            connection_error_shown = True
            display.draw_connection_error()
        time.sleep(10)

def run(config):
    
    display = kinky.inker(config)
    #display = kinky.disker()

    # check internet connection
    logging.info('Await network')
    wait_for_internet_connection(display)

    logging.info('Fetching chart data')
    # fetch the chart data
    chartdata = currency_chart.chart_data(config)

    with io.BytesIO() as file_stream:
        logging.info('Formatting chart for display')

        # write mathplot fig to stream and open as a PIL image
        chartdata.write_to_stream(file_stream)
        file_stream.seek(0)
        plot_image = Image.open(file_stream)
        
        # find some empty graph space to place our text
        title_positions = [(60, 5), (210, 5), (140, 5), (60, 200), (210, 200), (140, 200)] 
        selectedArea = least_intrusive_position(plot_image, title_positions)
        
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
        
        # add a border to the display
        draw_plot_image.rectangle([(0, 0), (display.WIDTH -1, display.HEIGHT-1)], outline='red')
        
        logging.info("Displaying image")
        display.show(plot_image) 
