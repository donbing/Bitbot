from src import bitbot
import configparser, sched, time, sys, logging, logging.config, pathlib, os
from os.path import join as pjoin

curdir = pathlib.Path(__file__).parent.resolve()

# load logging config
logging.config.fileConfig(pjoin(curdir, 'logging.ini'))
log_output_file = pjoin(curdir, 'debug.log')
logging.info("App starting")

# load app config
config_path = pjoin(curdir, 'config.ini')
config = configparser.ConfigParser()
config.read(config_path, encoding='utf-8')
logging.info("Loaded config from " + config_path)

# log unhandled exceptions
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
sys.excepthook = handle_exception

# configure bitbot chart updater
chart_updater = bitbot.chart_updater(config) 
def update_chart():
    chart_updater.run()
    if os.getenv('BITBOT_SHOWIMAGE') == 'true':
        os.system("code last_display.png")    

# terminate after test run
if os.getenv('TESTRUN') == 'true':
    update_chart()
    raise SystemExit

# schedule chart updates
scheduler = sched.scheduler(time.time, time.sleep)
secs_per_min = 60

def refresh_chart(sc): 
    update_chart()
    refresh_minutes = float(config['display']['refresh_time_minutes'])
    logging.info("Next refresh in: " + str(refresh_minutes) + " mins")
    sc.enter(refresh_minutes * secs_per_min, 1, refresh_chart, (sc,))

# update chart immediately and begin update schedule
refresh_chart(scheduler)
scheduler.run()
logging.info("Scheduler running")