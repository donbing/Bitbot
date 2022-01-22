
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
import os.path as path
from src.log_decorator import info_log
import logging

watched_files = {}

@info_log
def watch_config_dir(config_dir_path, on_changed):
    event_handler = ConfigChangeHandler(on_changed)
    observer = Observer()
    observer.schedule(event_handler, config_dir_path)
    observer.start()

class ConfigChangeHandler(FileSystemEventHandler):
    def __init__(self, on_changed):
        self.on_changed = on_changed

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
                self.on_changed()
            else:
                logging.info('file not really changed')