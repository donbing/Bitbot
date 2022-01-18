import pathlib, logging, logging.config
from os.path import join as pjoin
curdir = pathlib.Path(__file__).parent.resolve()
config_dir = pjoin(curdir, 'config')

# load logging config
logging.config.fileConfig(pjoin(config_dir, 'logging.ini'))
logging.info("App starting")

import configparser
# load app config
config_ini_path = pjoin(config_dir, 'config.ini')
config = configparser.ConfigParser()
config.read(config_ini_path, encoding='utf-8')
logging.info("Loaded config from " + config_ini_path)

from src import bitbot
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
import sched, time, sys,  os
import os.path as path

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

from hashlib import md5

# watch for changes to logfile
scheduler_event = None
watched_files = {}

class ConfigChangeHandler(FileSystemEventHandler):
     def on_modified(self, event):
        global watched_files
        if isinstance(event, FileModifiedEvent):
            file_path = event.src_path
            last_modified = path.getmtime(file_path)
            
            cached_last_modified = watched_files.get(file_path)
         
            new_change = file_path not in watched_files
            file_changed = last_modified != cached_last_modified

            if new_change or file_changed:
                logging.info('Config changed')
                watched_files[file_path] = last_modified
                # reload the app config
                config.read(config_ini_path, encoding='utf-8')
                # reload log config
                logging.config.fileConfig(pjoin(config_dir, 'logging.ini'))
                # restart schedule and refresh screen for event in self.scheduler.queue:
                for event in scheduler.queue:
                    try:
                        scheduler.cancel(event)
                    except ValueError:
                        # This is OK because the event may have been just canceled
                        pass
                refresh_chart(scheduler)

event_handler = ConfigChangeHandler()
observer = Observer()
observer.schedule(event_handler, config_dir)
observer.start()
logging.info("config observer ready")

# update chart immediately and begin update schedule
refresh_chart(scheduler)
scheduler.run()