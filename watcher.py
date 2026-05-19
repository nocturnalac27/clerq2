import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from core.renamer import Renamer
from core.history import HistoryLog

logger = logging.getLogger(__name__)


class DownloadHandler(FileSystemEventHandler):
    def __init__(self, config: dict, renamer: Renamer, history: HistoryLog):
        self.config = config
        self.renamer = renamer
        self.history = history

    def on_created(self, event):
        if event.is_directory:
            return

        filepath = event.src_path
        ext = os.path.splitext(filepath)[1].lower()

        # skip if extension not enabled
        if ext not in self.config.get("enabled_extensions", []):
            logger.debug(f"Skipping {filepath} — extension not enabled")
            return

        # skip if file is too large
        try:
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            if size_mb > self.config.get("max_file_size_mb", 50):
                logger.debug(f"Skipping {filepath} — too large ({size_mb:.1f}MB)")
                return
        except FileNotFoundError:
            return

        # skip if already renamed by clerq
        if self.history.already_processed(filepath):
            logger.debug(f"Skipping {filepath} — already processed")
            return

        # skip if folder is blacklisted
        folder = os.path.dirname(filepath)
        for bl in self.config.get("blacklisted_folders", []):
            if folder.startswith(os.path.expanduser(bl)):
                logger.debug(f"Skipping {filepath} — blacklisted folder")
                return

        # wait briefly for file to finish writing
        time.sleep(1.5)

        self.renamer.rename(filepath)


class FolderWatcher:
    def __init__(self, config: dict):
        self.config = config
        self.history = HistoryLog()
        self.renamer = Renamer(config, self.history)
        self.observer = Observer()
        self._paused = False

    def start(self):
        folders = self.config.get("watched_folders", ["~/Downloads"])
        recursive = self.config.get("watch_subfolders", False)

        for folder in folders:
            path = os.path.expanduser(folder)
            if not os.path.exists(path):
                logger.warning(f"Watched folder does not exist: {path}")
                continue
            handler = DownloadHandler(self.config, self.renamer, self.history)
            self.observer.schedule(handler, path, recursive=recursive)
            logger.info(f"Watching: {path}")

        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

    def pause(self):
        self._paused = True
        self.observer.stop()

    def resume(self):
        self._paused = False
        self.observer.start()

    @property
    def is_paused(self):
        return self._paused
