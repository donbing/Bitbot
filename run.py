from src import update_chart
import configparser
import sched, time
import logging, logging.config
import pathlib
from os.path import join as pjoin

curdir = pathlib.Path(__file__).parent.resolve()

# load logging config
logging.config.fileConfig(pjoin(curdir, 'logging.ini'))
log_output_file = pjoin(curdir, 'debug.log')

# load app config
config_path = pjoin(curdir, 'config.ini')
config = configparser.ConfigParser()
config.read(config_path, encoding='utf-8')
logging.info("Loaded config from " + config_path)

# schedule chart updates
scheduler = sched.scheduler(time.time, time.sleep)
chart_updater = update_chart.bitbot(config) 

def refresh_chart(sc): 
    chart_updater.run()
    refresh_minutes = float(config['display']['refresh_time_minutes'])
    logging.info("Next refresh in: " + str(refresh_minutes) + " mins")
    sc.enter(refresh_minutes * 60, 1, refresh_chart, (sc,))

# update chart immediately and begin update schedule
refresh_chart(scheduler)
scheduler.run()
logging.info("Scheduler running")