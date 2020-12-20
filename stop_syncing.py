import json
import os
import sys

DATA_DIR = os.path.expanduser("~/.pdfsync")
STARTUP_FILE = os.path.join(DATA_DIR, "to_sync.json")

def stop_syncing(source, destination):

    ### Remove the entry from the startup file

    if os.path.isfile(STARTUP_FILE):
        with open(STARTUP_FILE, "r+", encoding="utf8") as file:
            to_sync = json.load(file)
            if destination in to_sync[source]:
                to_sync[source].remove(destination)
                file.truncate(0)
                json.dump(to_sync, file)

    ### Kill the corresponding process

    ### TODO: How do we do this?
