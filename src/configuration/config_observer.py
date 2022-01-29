
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
from src.configuration.log_decorator import info_log
import hashlib

BLOCK_SIZE = 65536


def get_hash(file_path):
    file_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = f.read(BLOCK_SIZE)
    return file_hash.hexdigest()


@info_log
def watch_config_dir(config_dir_path, on_changed):
    event_handler = ConfigChangeHandler(on_changed)
    observer = Observer()
    observer.schedule(event_handler, config_dir_path)
    observer.start()


class ConfigChangeHandler(FileSystemEventHandler):
    def __init__(self, on_changed):
        self.on_changed = on_changed
        self.watched_files = {}

    def on_modified(self, event):
        if isinstance(event, FileModifiedEvent):
            file_path = event.src_path

            file_hash = get_hash(file_path)
            cached_file_hash = self.watched_files.get(file_path)

            new_change = file_path not in self.watched_files
            file_changed = file_hash != cached_file_hash

            if new_change or file_changed:
                self.config_changed(file_path, file_hash)

    @info_log
    def config_changed(self, file_path, file_hash):
        self.watched_files[file_path] = file_hash
        self.on_changed()
