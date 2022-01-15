from src import update_chart
import configparser
import pathlib
from os.path import join as pjoin
import sched, time
import logging, logging.handlers

curdir = pathlib.Path(__file__).parent.resolve()
log_path = pjoin(curdir, 'debug.log')
# setup our logger for std out and rolling file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.handlers.RotatingFileHandler(log_path, maxBytes=2000, backupCount=0),
        logging.StreamHandler()
    ])
logging.info("logging to " + log_path)

# get the config file data
filePath = pathlib.Path(__file__).parent.absolute()
config_path = str(filePath)+'/config.ini'
config = configparser.ConfigParser()
config.read(config_path)
logging.info("Loaded config from " + config_path)

# schedule chart updates
scheduler = sched.scheduler(time.time, time.sleep)

def get_refresh_rate_minutes():
     return float(config['display']['refresh_time_minutes'])
    
bb = update_chart.bitbot(config) 

def refresh_chart(sc): 
    bb.run()
    logging.info("Screen update complete")
    refresh_minutes = get_refresh_rate_minutes()
    logging.info("Next refresh in: " + str(refresh_minutes) + " mins")
    sc.enter(refresh_minutes * 60, 1, refresh_chart, (sc,))

# update chart immediately and begin update schedule
refresh_chart(scheduler)
scheduler.run()
logging.info("Scheduler running")