
from PIL import Image


# 🎨 create a limited pallete image for converting our image
def quantise_image(image, palette):
    palette_img = Image.new("P", (1, 1))
    palette_img.putpalette(palette + (0, 0, 0) * 252)
    return image.convert('RGB').quantize(palette=palette_img)
