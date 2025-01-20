from PIL import Image, ImageChops, ImageOps
from src.configuration.bitbot_files import use_config_dir
from src.configuration.bitbot_config import load_config_ini
from src.bitbot import BitBot
import os
import pathlib
import unittest

# check config files
curdir = pathlib.Path(__file__).parent.resolve()
files = use_config_dir(os.path.join(curdir, "../"))


# physical screen renderers for approval testing
class screen_output_renderers:
    wave27b = {'output': 'waveshare.epd2in7b_V2'}
    inky = {'output': 'inky'}


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


# test-specific config
test_configs = {
    "APPLE_1mo_defaults": {
        'currency': {'stock_symbol': 'AAPL'},
        'display': {'candle_width': '1mo'},
    },
    "TSLA_3mo_defaults": {
        'currency': {
            'chart_since': '2016-04-22T00:00Z',
            'stock_symbol': 'TSLA'
        },        
        'display': {'candle_width': '3mo'},
    },
    "MSFT_3mo_defaults_with_entry": {
        'display': {'candle_width': '3mo'},
        'currency': {
            'stock_symbol': 'MSFT',
            'entry_price': '167',
            'chart_since': '2016-04-22T00:00Z', # yfinance limits to gathering 7 days of low-timeframe from the last 60 days
            'holdings': '10',
        },
    },
    "AUDCAD_3mo_defaults_with_entry": {
        'currency': {
            'stock_symbol': 'AUDCAD=X',
            'entry_price': '0.89332',
            'chart_since': '2020-04-22T00:00Z', # yfinance limits to gathering 7 days of low-timeframe from the last 60 days
            'holdings': '450000',
        },
        'display': {'candle_width': '1mo', },
    },
    "BTC_5m_defaults": {
        'display': {'candle_width': '5m'},
    },
    "BTC_1h_defaults": {
        'display': {'candle_width': '1h'},
    },
    "BTC_1h_100K": {
        'display': {'candle_width': '1h'},
        'currency': {'chart_since': '2023-11-10T00:00Z'},
    },
    "BTC_1d_defaults": {
        'display': {'candle_width': '1d'},
        'currency': {'chart_since': '2023-10-01T00:00Z'},
    },
    "BTC_HOLDINGS": {
        'currency': {'holdings': "100"},
    },
    "BTC_VOLUME": {
        'display': {'show_volume': 'true'},
    },
    "BTC_EXPANDED": {
        'display': {'expanded_chart': 'true'},
    },
    "BTC_VOLUME_EXPANDED": {
        'display': {'show_volume': 'true', 'expanded_chart': 'true'},
    },
    "BTC_VOLUME_OVERLAY2": {
        'display': {'overlay_layout': '2', 'show_volume': 'true'},
    },
    "BTC_OVERLAY2": {
        'display': {'overlay_layout': '2'},
    },
    "bitmex_ETH_5m_defaults": {
        'currency': {'instrument': 'ETH/USD'},
        'display': {'candle_width': '5m'},
    },
    "bitmex_ETH_1h_defaults": {
        'currency': {'instrument': 'ETH/USD'},
        'display': {'candle_width': '1h'},
    },
    "bitmex_ETH_1d_defaults": {
        'currency': {'instrument': 'ETH/USD'},
        'display': {'candle_width': '1d'},
    },
    "cryptocom_CRO_5m_defaults": {
        'currency': {'instrument': 'CRO/BTC', 'exchange': 'cryptocom'},
        'display': {'candle_width': '5m'},
    },
    "cryptocom_CRO_1h_defaults": {
        'currency': {'instrument': 'CRO/BTC', 'exchange': 'cryptocom'},
        'display': {'candle_width': '1h'},
    },
    "cryptocom_CRO_1d_defaults": {
        'currency': {
            'instrument': 'CRO/BTC',
            'exchange': 'cryptocom',
        },
        'display': {'candle_width': '1d'},
    },
}

os.makedirs('tests/images/', exist_ok=True)


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
        os.makedirs(fails_folder)
        diff_file_path = os.path.join(fails_folder, name)
        
        threshold = 128
        diff = diff.point(lambda x: 0 if x < threshold else 255)
        diff.save(diff_file_path)

        return diff, diff_file_path


class TestRenderingMeta(type):
    def __new__(mcs, name, bases, dict, output):
        def gen_test(generatedTestName, custom_config):
            def test(self):
                config = load_config_ini(files)
                config.read_dict(config_defaults)
                config.read_dict(custom_config)
                
                display_resolution = output.get('resolution', '')
                config.set('display', 'output', output['output'])
                config.set('display', 'resolution', display_resolution)

                file_path = f'tests/images/{display_resolution}/'
                os.makedirs(file_path, exist_ok=True)
                file_name = f'{file_path}/{generatedTestName}.png'

                config.set('display', 'disk_file_name', file_name)
                
                previous_image = Image.open(file_name) if os.path.isfile(file_name) else None

                app = BitBot(config, files)
                app.display_chart()

                new_image = Image.open(file_name)

                assert_image_matches_size(new_image, output.get('resolution', ''))

                changes = image_changes(previous_image, new_image, file_name)
                if changes:
                    os.system("code '" + file_name + "'")
                    # if changes[1] is not None:
                    #     os.system("code '" + changes[1] + "'")
                    assert False, f"Image diff check: '{changes}'"

            return test

        for test_key in test_configs:
            output_res = output['output'].split('.')[-1]
            screen_res = output.get('resolution', output_res)
            test_name = f"test_{screen_res}_{test_key}"
            dict[test_name] = gen_test(test_name, test_configs[test_key])

        return type.__new__(mcs, name, bases, dict)


class SmallChartRenderingTests(unittest.TestCase, output=disk_output_renderers.disk_small, metaclass=TestRenderingMeta):
    __metaclass__ = TestRenderingMeta


class MediumChartRenderingTests(unittest.TestCase, output=disk_output_renderers.disk_med, metaclass=TestRenderingMeta):
    __metaclass__ = TestRenderingMeta


class LargeChartRenderingTests(unittest.TestCase, output=disk_output_renderers.disk_large, metaclass=TestRenderingMeta):
    __metaclass__ = TestRenderingMeta


class ExtraLargeChartRenderingTests(unittest.TestCase, output=disk_output_renderers.disk_extra_large, metaclass=TestRenderingMeta):
    __metaclass__ = TestRenderingMeta


@unittest.skip("needs a waveshare display")
class Wave27bChartRenderingTests(unittest.TestCase, output=screen_output_renderers.wave27b, metaclass=TestRenderingMeta):
    __metaclass__ = TestRenderingMeta


@unittest.skip("needs an inky display")
class InkyChartRenderingTests(unittest.TestCase, output=screen_output_renderers.inky, metaclass=TestRenderingMeta):
    __metaclass__ = TestRenderingMeta
