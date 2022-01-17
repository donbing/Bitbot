from src import bitbot
import configparser, sched, time, sys, logging, logging.config, pathlib, os
from os.path import join as pjoin

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent

curdir = pathlib.Path(__file__).parent.resolve()
config_dir = pjoin(curdir, 'config')
# load logging config
logging.config.fileConfig(pjoin(config_dir, 'logging.ini'))
logging.info("App starting")

# load app config
config_ini_path = pjoin(config_dir, 'config.ini')
config = configparser.ConfigParser()
config.read(config_ini_path, encoding='utf-8')
logging.info("Loaded config from " + config_ini_path)

# watch for changes to logfile
scheduler_event = None
last_trigger_time = 0
class ConfigChangeHandler(FileSystemEventHandler):
     def on_modified(self, event):
        global last_trigger_time
        current_time = time.time()
        if isinstance(event, FileModifiedEvent) and (current_time - last_trigger_time) > 3:
            logging.info('Config modified ' + str(current_time - last_trigger_time))
            # reload the app config
            config.read(config_ini_path, encoding='utf-8')
            # reload log config
            logging.config.fileConfig(pjoin(config_dir, 'logging.ini'))
            # restart schedule and refresh screen
            scheduler.cancel(scheduler_event)
            refresh_chart(scheduler)
            last_trigger_time = current_time

event_handler = ConfigChangeHandler()
observer = Observer()
observer.schedule(event_handler, config_dir)
observer.start()
logging.info("config observer ready")

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
    global scheduler_event
    update_chart()
    refresh_minutes = float(config['display']['refresh_time_minutes'])
    logging.info("Next refresh in: " + str(refresh_minutes) + " mins")
    scheduler_event = sc.enter(refresh_minutes * secs_per_min, 1, refresh_chart, (sc,))

# update chart immediately and begin update schedule
refresh_chart(scheduler)
scheduler.run()
logging.info("Scheduler running")