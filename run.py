from src import update_chart
import configparser
import pathlib
import sched, time
import logging, logging.handlers

# setup our logger for std out and rolling file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.handlers.RotatingFileHandler("debug.log", maxBytes=2000, backupCount=0),
        logging.StreamHandler()
    ])
logging.info("Starting")

# get the config file data
filePath = pathlib.Path(__file__).parent.absolute()
config = configparser.ConfigParser()
config.read(str(filePath)+'/config.ini')
logging.info("Loaded config")

# schedule chart updates
scheduler = sched.scheduler(time.time, time.sleep)

def refresh_chart(sc): 
    update_chart.run(config)
    logging.info("Update complete")
    redfresh_minutes = config['display']['refresh_time_minutes']
    refresh_seconds = float(redfresh_minutes) * 60
    logging.info("Next refresh in: " + str(redfresh_minutes) + " mins")
    scheduler.enter(refresh_seconds, 1, refresh_chart, (sc,))

# update chart immediately and begin update schedule
update_chart.run(config)
logging.info("Initial screen update complete")
scheduler.enter(refresh_seconds, 1, refresh_chart, (scheduler,))
scheduler.run()
logging.info("Scheduler running")