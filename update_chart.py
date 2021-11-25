import bitmex_ccxt
import io
import inky 
import pathlib
from PIL import Image, ImageFont, ImageDraw
from pprint import pprint
import random
from inky import InkyWHAT
import RPi.GPIO as GPIO
import configparser

filePath = pathlib.Path(__file__).parent.absolute()
config = configparser.ConfigParser()
config.read('./config.ini')

# sort positions by average colour and then by random
def BestTextPositionFor(img, possibleTextPositions):
    rgb_im = img.convert('RGB')
    ordredByAveColour = sorted(title_positions, key=lambda item: (get_average_color(*item, 50, rgb_im), random.random()))
    return ordredByAveColour[-1]

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

print('starting..')
chartdata = bitmex_ccxt.chart_data(config)

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
    price_font = ImageFont.truetype(str(filePath)+'/04B_03__.TTF', 40)
    title_font = ImageFont.truetype(str(filePath)+'/04B_03__.TTF', 16)

    draw_plot_image = ImageDraw.Draw(plot_image)

    
    # instrument / time text
    draw_plot_image.text(selectedArea, 'BTC/$ (' + chartdata.candle_width + ')', (0,0,0), title_font)

    # % change text
    change = ((chartdata.last_close()-chartdata.start_price())/chartdata.last_close())*100
    draw_plot_image.text((selectedArea[0]+90, selectedArea[1]), '{:+.2f}'.format(change) + '%', (255 if change > 0 else 0,0,0), title_font)
    
    # current price text
    draw_plot_image.text((selectedArea[0], selectedArea[1]+11),'$' + '{:,.0f}'.format(chartdata.last_close()), (0,0,0), price_font)

    # select some random comment depending on price action
    if random.random() < .5:
        if chartdata.start_price() < chartdata.last_close():
            messages=config.get('comments', 'up').split(',')
        else:
            messages=config.get('comments', 'down').split(',')
        draw_plot_image.text((selectedArea[0], selectedArea[1]+48), random.choice(messages), (0,0,0), title_font)
   
    print("displaying image")

    # create a limited pallete image for converting our chart image to.
    pal_img = Image.new("P", (1, 1))
    pal_img.putpalette((255, 255, 255, 0, 0, 0, 255, 0, 0) + (0, 0, 0) * 252)

    # rotate the image and set 3 colour palette
    display_config = config["display"]
    image_rotation = display_config.getint("rotation")
    display_image = plot_image.rotate(image_rotation).convert('RGB').quantize(palette=pal_img)
    display_image.save('last_display.png')
    # create the display and show the image
    inky_display = InkyWHAT(display_config["colour"])
    inky_display.set_image(display_image) 
    inky_display.show()