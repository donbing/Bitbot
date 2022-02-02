
padding = 10

def draw_centered_text(draw, message, font, display_size, pos='centre'):
    # 🌌 calculate space needed for message
    message_size = draw.textsize(
        message,
        font)

    # 📏 where to position the message
    if pos == 'centre':
        message_x, message_y = center_aligned(display_size,  message_size)
    elif pos == 'topright':
        message_x, message_y = top_right_aligned(display_size,  message_size)
    elif pos == 'topleft':
        message_x, message_y = top_left_aligned(display_size,  message_size)

    # 🖊️ draw the message at position
    draw.multiline_text(
        (message_x, message_y),
        message,
        fill='black',
        font=font,
        align="left")

    # 📏 position  for surrounding box
    x0, y0 = (message_x - padding, message_y - padding)
    x1 = message_x + message_size[0] + padding
    y1 = message_y + message_size[1] + padding
    # 🖊️ draw box at position
    draw.rectangle([(x0, y0), (x1, y1)], outline='red')


def top_right_aligned(display_size, message_size):
    return (display_size[0] - message_size[0] - padding - 1, padding)


def top_left_aligned(display_size, message_size):
    return (0 + padding + 1, 0 + padding + 1)


def center_aligned(display_size, message_size):
    message_y = (display_size[1] - message_size[1]) / 2
    message_x = (display_size[0] - message_size[0]) / 2
    return (message_y, message_x)
