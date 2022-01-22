import pathlib, logging, logging.config, sched, time, sys, os
from os.path import join as pjoin
from src.configuration.bitbot_files import use_config_dir  
from src.configuration.bitbot_config import load_config_ini 
from src.configuration.bitbot_logging import initialise_logger 
from src.configuration.config_observer import watch_config_dir 

# declare config files
config_files = use_config_dir(pathlib.Path(__file__).parent.resolve())
# load logging config
initialise_logger(config_files.logging_ini)
# load app config
config = load_config_ini(config_files.config_ini)

from src import bitbot

# create bitbot chart updater
chart_updater = bitbot.chart_updater(config)
def update_chart():
    chart_updater.run()
    # show image in vscode for debug
    if os.getenv('BITBOT_SHOWIMAGE') == 'true':
        os.system("code last_display.png")    

# schedule chart updates
scheduler = sched.scheduler(time.time, time.sleep)
secs_per_min = 60

def refresh_chart(sc): 
    global scheduler_event
    update_chart()
    # dont reschedule if testing
    if os.getenv('TESTRUN') != 'true':
        refresh_minutes = config.refresh_rate_minutes()
        logging.info("Next refresh in: " + str(refresh_minutes) + " mins")
        scheduler_event = sc.enter(refresh_minutes * secs_per_min, 1, refresh_chart, (sc,))

# watch for changes to logfile
scheduler_event = None

def config_changed():
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

watch_config_dir(config_files.config_folder, refresh_chart)

# update chart immediately and begin update schedule
refresh_chart(scheduler)
scheduler.run()