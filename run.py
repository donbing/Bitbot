from src import update_chart
import configparser
import pathlib

filePath = pathlib.Path(__file__).parent.absolute()
config = configparser.ConfigParser()
config.read(str(filePath)+'/config.ini')

update_chart.run(config)