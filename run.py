from src import update_chart
import configparser
import pathlib
import sched, time
import logging, logging.handlers

# setup our logger for std out and rolling file
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.handlers.RotatingFileHandler("debug.log", maxBytes=2000, backupCount=10),
        logging.StreamHandler()
    ])
logging.info("starting")

# get the config file data
filePath = pathlib.Path(__file__).parent.absolute()
config = configparser.ConfigParser()
config.read(str(filePath)+'/config.ini')
logging.debug("loaded config")

# schedule chart updates
redfresh_minutes = config['display']['refresh_time_minutes']
refresh_seconds = float(redfresh_minutes) * 60
logging.info("refreshing every: " + str(redfresh_minutes) + " mins")
scheduler = sched.scheduler(time.time, time.sleep)

def do_something(sc): 
    logging.debug("refreshing")
    update_chart.run(config)
    scheduler.enter(refresh_seconds, 1, do_something, (sc,))

# update chart immediately and begin update schedule
update_chart.run(config)
scheduler.enter(refresh_seconds, 1, do_something, (scheduler,))
scheduler.run()

logging.debug("update scheduler running")