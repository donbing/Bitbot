from .Align import Align
from . import padding


def centered_text(draw, text, font, container_size, pos='centre', border=False):
    # 🌌 calculate space needed for message
    message_size = max(font.getbbox(line)[-2:] for line in text.split('\n'))

    # 📏 where to position the message
    if pos == 'centre':
        message_y, message_x  = Align.Centre(container_size, message_size)
    elif pos == 'topright':
        message_y, message_x = Align.TopRight(container_size, message_size)
    elif pos == 'topleft':
        message_y, message_x = Align.TopLeft(container_size, message_size)

    # 🖊️ draw the message at position
    draw.multiline_text(
        (message_y, message_x),
        text,
        fill='black',
        font=font,
        align="left")
    
    # 📏 measure border box
    if border:
        y0, x0 = (message_y - padding, message_x - padding)
        y1 = message_y + message_size[0] + padding
        x1 = message_x + message_size[1] + padding
        # 🖊️ draw box at position
        draw.rectangle([(y0, x0), (y1, x1)], outline='red')
