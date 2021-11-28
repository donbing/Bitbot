from src import update_chart
import configparser


config = configparser.ConfigParser()
config.read('./config.ini')

update_chart.run(config)