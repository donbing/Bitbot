from datetime import timedelta
from datetime import datetime
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
from src.input.buttons import Buttons
from src.bitbot import BitBot
from src.drawing.intro import IntroPlayer
from src.display.picker import picker

# 🗂️ declare config files
config_files = use_config_dir(pathlib.Path(__file__).parent.resolve())

# 🪵 load logging config
initialise_logger(config_files.logging_ini)
logging.info(f"app: start")

# ⚙️ load app config
config = load_config_ini(config_files)

# 📈 create bitbot chart updater
app = BitBot(config, config_files)

# 🎁 oobex
display = picker(config)
config.on_first_run(lambda: IntroPlayer(display, config))

# 👉 button handlers
buttons = Buttons(config)


@info_log
def refresh_display(sc, reason):
    now = datetime.now()
    # 🖼️ in picture frame mode, do not refresh on schedule
    if config.photo_mode_enabled():
        if reason != "scheduled":
            app.display_photo()
    elif config.youtube_subs_enabled():
        app.display_youtube_subs()
    elif config.tide_times_enabled():
        app.display_tide_times()
    elif config.multiple_instruments():
        app.cycle_chart()
    elif config.today_has_special_message(now):
        app.display_message(config.special_message(now))
    elif config.text_message_enabled():
        app.display_message(config.text_message())
    else:
        app.display_chart()
        
    # 🪳 show image in vscode for debug
    if config.shoud_show_image_in_vscode():
        os.system("code pictures/last_display.png")

   # ⌛ dont reschedule if testing
    if not config.is_test_run():
        re_schedule(timedelta(minutes=config.refresh_rate_minutes()), sc)


@info_log
def re_schedule(refresh_intervale, sc):
    sc.enter(refresh_intervale.seconds, 1, lambda s: refresh_display(s, "scheduled"), (sc,))


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
