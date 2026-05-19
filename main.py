import threading
from core.watcher import FolderWatcher
from core.config import load_config
from ui.tray import TrayApp


def main():
    config = load_config()

    watcher = FolderWatcher(config)
    watcher_thread = threading.Thread(target=watcher.start, daemon=True)
    watcher_thread.start()

    app = TrayApp(config, watcher)
    app.run()


if __name__ == "__main__":
    main()
