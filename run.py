import pathlib, logging, logging.config, sched, time, sys, os
from os.path import join as pjoin
from src.configuration.bitbot_files import use_config_dir  
from src.configuration.bitbot_config import load_config_ini 
from src.configuration.bitbot_logging import initialise_logger 

# declare config files
config_files = use_config_dir(pathlib.Path(__file__).parent.resolve())
# load logging config
initialise_logger(config_files.logging_ini)
# load app config
config = load_config_ini(config_files.config_ini)

from src import bitbot
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
import os.path as path

# create bitbot chart updater
chart_updater = bitbot.chart_updater(config)

def update_chart():
    chart_updater.run()
    # show image in vscode for debug
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
                config.reload(config_files.config_ini)
                # restart schedule and refresh screen for event in self.scheduler.queue:
                for event in scheduler.queue:
                    try:
                        scheduler.cancel(event)
                    except ValueError:
                        # This is OK because the event may have been just canceled
                        pass
                refresh_chart(scheduler)
            else:
                logging.info('file not really changed')

event_handler = ConfigChangeHandler()
observer = Observer()
observer.schedule(event_handler, config_files.base_path)
observer.start()
logging.info("config observer ready")

# update chart immediately and begin update schedule
refresh_chart(scheduler)
scheduler.run()