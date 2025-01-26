import io
from PIL import Image, ImageChops
import pandas as pd
from src.configuration.bitbot_files import use_config_dir
from src.configuration.bitbot_config import load_config_ini
import os
import pathlib
import unittest

from src.drawing.market_charts.mpf_plotted_chart import MplFinanceChart
from src.exchanges.CandleData import CandleData

# check config files
curdir = pathlib.Path(__file__).parent.resolve()
files = use_config_dir(os.path.join(curdir, "../"))


# physical screen renderers for approval testing
class screen_output_renderers:
    wave27b = {'output': 'waveshare.epd2in7b_V2'}
    inky = {'output': 'inky'}


exchange_name = "coinbase"
test_currencies = ["ETH/USD", "BTC/USD"]
display_sizes = ["264x176", "400x300", "640x448", "800x480"]

# s/m/l image file renderers for automated testing
class disk_output_renderers:
    disk_small = {'output': 'disk', 'resolution': "264x176"}
    disk_med = {'output': 'disk', 'resolution': "400x300"}
    disk_large = {'output': 'disk', 'resolution': "640x448"}
    disk_extra_large = {'output': 'disk', 'resolution': "800x480"}
    all = [disk_small, disk_med, disk_large]


# basic config
config_defaults = {
    'currency': {
        'stock_symbol': '',
        'exchange': 'coinbase',
        'instrument': 'BTC/USD',
        'holdings': '0',
        'chart_since': '2022-11-22T00:00Z',
        'entry_price': 0,
    },
    'display': {
        'output': 'disk',
        'resolution': '400x300',
        'overlay_layout': '1',
        'expanded_chart': 'false',
        'show_volume': 'falsae',
        'candle_width': '1h',
        'rotation': '0',
        'show_ip': 'false',
        'timestamp': 'false',
    },
    'comments': {
        'up': 'moon',
        'down': 'doom',
    }
}


def assert_image_matches_size(new_image, expected_res):
    actual_res = f"{new_image.width}x{new_image.height}"
    assert expected_res == actual_res, f"expected {expected_res}, was {actual_res}"


def image_changes(previous_image, new_image, file_name):
    if previous_image is None:
        return new_image
    diff = ImageChops.difference(new_image.convert('RGB'), previous_image.convert('RGB'))

    differenceImageBounds = diff.getbbox()
    if differenceImageBounds:
        dir, name, = os.path.split(file_name)
        fails_folder = os.path.join(dir, 'fail')
        os.makedirs(fails_folder, exist_ok=True)
        diff_file_path = os.path.join(fails_folder, name)

        threshold = 128
        diff = diff.point(lambda x: 0 if x < threshold else 255)
        diff.save(diff_file_path)

        return diff, diff_file_path

class TestDisplay():
    def size(self):
        return (400,300)
    
    def dpi(self):
        return 100

class TestRenderingMeta(type):
    def __new__(mcs, name, bases, dict, output):

        def gen_test(generatedTestName, config, data_file_name):
            def test(self):
                # arrangement
                price_history = pd.read_pickle(f"tests/data/{data_file_name}")
                source, dest, candle_width = data_file_name.replace(".pkl", "").split("_")
                
                chart_data = CandleData(f"{source}/{dest}", candle_width, price_history)

                test_image_file_path = f"tests/images/{generatedTestName}.png"

                previous_image = Image.open(test_image_file_path) if os.path.exists(test_image_file_path) else None

                # action
                chart = MplFinanceChart(
                    config, 
                    TestDisplay(), 
                    files)

                with io.BytesIO() as file_stream:
                    chart.write_to_stream(file_stream, chart_data)
                    chart_image = Image.open(file_stream)
                    chart_image.save(test_image_file_path)
                    
                    # assertion
                    assert_image_matches_size(chart_image, "400x300")

                    changes = image_changes(previous_image, chart_image, file_name)
                    if changes:
                        os.system("code '" + test_image_file_path + "'")
                        # if changes[1] is not None:
                        #     os.system("code '" + changes[1] + "'")
                        assert False, f"Image diff check: '{changes}'"

            return test

        os.makedirs('tests/images/', exist_ok=True)

        config = load_config_ini(files)
        config.read_dict(config_defaults)
        for file_name in os.listdir("tests/data/"):
            test_name = f"test_{file_name}".replace(".pkl","")
            dict[test_name] = gen_test(test_name, config, file_name)

        return type.__new__(mcs, name, bases, dict)


class SmallChartRenderingTests(unittest.TestCase, output=disk_output_renderers.disk_small, metaclass=TestRenderingMeta):
    __metaclass__ = TestRenderingMeta


# class MediumChartRenderingTests(unittest.TestCase, output=disk_output_renderers.disk_med, metaclass=TestRenderingMeta):
#     __metaclass__ = TestRenderingMeta


# class LargeChartRenderingTests(unittest.TestCase, output=disk_output_renderers.disk_large, metaclass=TestRenderingMeta):
#     __metaclass__ = TestRenderingMeta


# class ExtraLargeChartRenderingTests(unittest.TestCase, output=disk_output_renderers.disk_extra_large, metaclass=TestRenderingMeta):
#     __metaclass__ = TestRenderingMeta


# @unittest.skip("needs a waveshare display")
# class Wave27bChartRenderingTests(unittest.TestCase, output=screen_output_renderers.wave27b, metaclass=TestRenderingMeta):
#     __metaclass__ = TestRenderingMeta


# @unittest.skip("needs an inky display")
# class InkyChartRenderingTests(unittest.TestCase, output=screen_output_renderers.inky, metaclass=TestRenderingMeta):
#     __metaclass__ = TestRenderingMeta
