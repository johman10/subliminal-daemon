import sys
import logging
import time
import os
import mimetypes
from datetime import timedelta
from babelfish import Language
from subliminal import region, save_subtitles, scan_video, ProviderPool, provider_manager
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv

load_dotenv()
region.configure('dogpile.cache.dbm', arguments={'filename': 'cachefile.dbm'})
logging.basicConfig(level=logging.DEBUG)

DIRECTORIES = os.getenv("WATCHDOG_DIRECTORIES").split(",")
PROVIDERS = [
    'legendastv',
    'opensubtitles',
    'podnapisi',
    'shooter',
    'thesubdb',
    'tvsubtitles'
]
PROVIDER_CONFIGURATIONS = {
    'legendastv': {
        'username': os.getenv("LEGENDASTV_USER"),
        'password': os.getenv("LEGENDASTV_PASS")
    },
    'opensubtitles': {
        'username': os.getenv("OPENSUBTITLES_USER"),
        'password': os.getenv("OPENSUBTITLES_PASS")
    },
}
ENABLED_PROVIDERS = list(filter(lambda p: os.getenv(f"{p.upper()}_ENABLED", "true") == "true", PROVIDERS))
provider_pool = ProviderPool(providers=ENABLED_PROVIDERS, provider_configs=PROVIDER_CONFIGURATIONS)

class Watcher:
    def __init__(self):
        self.observer = Observer()

    def start(self):
        event_handler = SubliminalClient()
        for directory in DIRECTORIES:
            self.observer.schedule(event_handler, directory, recursive=True)

        self.observer.start()

        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            logging.error(f"Error: {sys.exc_info()[0]}")

        self.observer.join()


class SubliminalClient(FileSystemEventHandler):
    @staticmethod
    def on_created(event):
        if event.is_directory:
            return

        path = event.src_path

        if not mimetypes.guess_type(path)[0].startswith('video'):
            return

        logging.debug(f"Pulling subtitles for: {path}")
        video = scan_video(path)
        subtitles = provider_pool.list_subtitles(video=video, languages={Language('eng'), Language('nld')})
        best_subtitles = provider_pool.download_best_subtitles(subtitles=subtitles, video=video, languages={Language('eng'), Language('nld')})
        save_subtitles(video, best_subtitles)


if __name__ == '__main__':
    logging.debug("Start up")
    watcher = Watcher()
    watcher.start()
