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
from src.buttons import Buttons
from src.bitbot import BitBot
from src.intro import IntroPlayer
from src.display.kinky import picker

# 🗂️ declare config files
config_files = use_config_dir(pathlib.Path(__file__).parent.resolve())
# 🪵 load logging config
initialise_logger(config_files.logging_ini)
# ⚙️ load app config
config = load_config_ini(config_files)
# 📈 create bitbot chart updater
app = BitBot(config, config_files)
# 👉 button handlers
buttons = Buttons(config)

# oobex
config.on_first_run(lambda: IntroPlayer(picker(config), config))


@info_log
def refresh_display(sc, reason):
    # 🖼️ in picture frame mode, do not refresh on schedule
    if config.photo_mode_enabled():
        if reason != "scheduled":
            app.display_photo()
    else:
        app.display_chart()
        # 🪳 show image in vscode for debug
        if config.shoud_show_image_in_vscode():
            os.system("code last_display.png")

    # ⌛ dont reschedule if testing
    if not config.is_test_run():
        refresh_minutes = config.refresh_rate_minutes()
        logging.info("Next refresh in: " + str(refresh_minutes) + " mins")
        sc.enter(
            refresh_minutes * 60,
            1,
            lambda s: refresh_display(s, "scheduled"),
            (sc,))


@info_log
def cancel_schedule(sc):
    for event in sc.queue:
        try:
            sc.cancel(event)
        except ValueError:
            # This is OK because the event may have been just canceled
            pass


def config_changed(sc, reason):
    # 🔁 reload the app config
    config.reload()
    # 🚫 cancel current schedule
    cancel_schedule(sc)
    # ⏳ new schedule
    refresh_display(sc, reason)


# ⏳ scheduler for regular chart updates
scheduler = sched.scheduler(time.time, time.sleep)

# 🔁 refresh chart on config file change
watch_config_dir(
    config_files.config_folder,
    on_changed=lambda: config_changed(scheduler, "file_change"))

# 🚦 update chart immediately and begin schedule
refresh_display(scheduler, "startup")
scheduler.run()
