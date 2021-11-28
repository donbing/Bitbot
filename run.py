from src import update_chart
import configparser

config = configparser.ConfigParser()
config.read('./config.ini')
print("loaded config")
update_chart.run(config)