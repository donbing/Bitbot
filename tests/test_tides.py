import io
import unittest
from src.drawing.tide_times import tidal_graph
from PIL import Image, ImageDraw

class TestTidalGraph(unittest.TestCase):

    def test_data_fetch_and_render(self):
        
        with io.BytesIO() as img_buf:
            tidal_graph.render_tide_chart("0184", img_buf)
            
            image = Image.open(img_buf)
            image.save(f'tests/images/TidalGraph.png')
