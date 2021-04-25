import bitmex_ccxt
import io
import inky 
import pathlib
from PIL import Image, ImageFont, ImageDraw
from pprint import pprint
import random
from inky import InkyWHAT
import RPi.GPIO as GPIO

filePath = pathlib.Path(__file__).parent.absolute()

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

chartdata = bitmex_ccxt.chart_data()

with io.BytesIO() as file_stream:
    print('Formatting image for display')
    # write mathplot fig to stream
    chartdata.fig.savefig(file_stream, dpi=chartdata.fig.dpi)
    file_stream.seek(0)
    # open image from stream and limit to 3 colors
    plot_image = Image.open(file_stream)
    
    title_positions = [(40, 20), (40, 220), (210, 20), (210, 220)]
    selectedArea = BestTextPositionFor(plot_image, title_positions)
    
    price_font = ImageFont.truetype(str(filePath)+'/04B_03__.TTF', 48)
    title_font = ImageFont.truetype(str(filePath)+'/04B_03__.TTF', 16)
    draw_plot_image = ImageDraw.Draw(plot_image)
    width = chartdata.candle_width
    draw_plot_image.text(selectedArea, 'BTC/$ (' + width + ')', 2, title_font)
    draw_plot_image.text((selectedArea[0], selectedArea[1]+11),'{:.2f}'.format(chartdata.last_close() / 1000) + 'K', 1, price_font)

    if random.random() < .5:
        if chartdata.start_price() < chartdata.end_price():
            messages=["moon", "yolo", "pump it", ""]
        else:
            messages=["short the corn!", "goblin town", "blood in the streets", "dooom", "sell!!"]
        draw_plot_image.text((selectedArea[0], selectedArea[1]+48), random.choice(messages), 2, title_font)
   
    # turn the image upside down for display
    inky_display = InkyWHAT("yellow")
    inky_display.set_image(plot_image.convert('P', palette=Image.ADAPTIVE, colors=3)) #plot_image.rotate(180)
    inky_display.show()
    print("saving image")
    plot_image.save("candle2.png")
    # display
