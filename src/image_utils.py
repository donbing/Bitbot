def draw_centered_text(draw, message, title_font, display_size):
    # 🌌 calculate space needed for message
    message_width, message_height = draw.textsize(
        message,
        title_font)
    # 📏 where to position the message
    message_y = (display_size[1] - message_height) / 2
    message_x = (display_size[0] - message_width) / 2
    # 🖊️ draw the message at position
    draw.multiline_text(
        (message_x, message_y),
        message,
        fill='black',
        font=title_font,
        align="center")
    # 📏 position  for surrounding box
    padding = 10
    x0, y0 = (message_x - padding, message_y - padding)
    x1 = message_x + message_width + padding
    y1 = message_y + message_height + padding
    # 🖊️ draw box at position
    draw.rectangle([(x0, y0), (x1, y1)], outline='red')
