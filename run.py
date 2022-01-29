import pathlib
import logging
import logging.config
import sched
import time
import os
from src.configuration.bitbot_files import use_config_dir
from src.configuration.bitbot_config import load_config_ini
from src.configuration.bitbot_logging import initialise_logger
from src.configuration.config_observer import watch_config_dir
from src.configuration.log_decorator import info_log
from src.bitbot import BitBot

# declare config files
config_files = use_config_dir(pathlib.Path(__file__).parent.resolve())
# load logging config
initialise_logger(config_files.logging_ini)
# load app config
config = load_config_ini(config_files.config_ini)
# create bitbot chart updater
app = BitBot(config, config_files)


@info_log
def refresh_chart(sc):
    app.run()
    # show image in vscode for debug
    if config.shoud_show_image_in_vscode():
        os.system("code last_display.png")
    # dont reschedule if testing
    if not config.is_test_run():
        refresh_minutes = config.refresh_rate_minutes()
        logging.info("Next refresh in: " + str(refresh_minutes) + " mins")
        sc.enter(refresh_minutes * 60, 1, refresh_chart, (sc,))


@info_log
def cancel_schedule(sc):
    for event in sc.queue:
        try:
            sc.cancel(event)
        except ValueError:
            # This is OK because the event may have been just canceled
            pass


@info_log
def config_changed(sc):
    # reload the app config
    config.reload(config_files.config_ini)
    # cancel current schedule
    cancel_schedule(sc)
    # new schedule
    refresh_chart(sc)


# scheduler for regular chart updates
scheduler = sched.scheduler(time.time, time.sleep)

# refresh chart on config file change
watch_config_dir(
    config_files.config_folder,
    on_changed=lambda: config_changed(scheduler))

# update chart immediately and begin schedule
refresh_chart(scheduler)
scheduler.run()
