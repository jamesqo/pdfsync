import json
import os
import time
import subprocess
import sys

from sync_once import sync_once

DATA_DIR = ...
STARTUP_FILE = ...

def start_syncing(source, destination):

    ### Create the startup file if it doesn't exist

    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.isfile(STARTUP_FILE):
        with open(STARTUP_FILE, "w", encoding="utf8") as file:
            file.write("{}")

    ### Add the entry to the startup file

    with open(STARTUP_FILE, "r+", encoding="utf8") as file:
        to_sync = json.load(file)
        if source not in to_sync:
            to_sync[source] = [destination]
        elif destination not in to_sync[source]:
            to_sync[source] = sorted(to_sync[source] + [destination])
        file.truncate(0)
        json.dump(to_sync, file)
    
    ### Sync once immediately

    sync_once(source, destination)

    ### Sync every time an hour passes
    # TODO: Make use of the APIs at
    # - https://developers.google.com/drive/api/v3/reference/changes/watch
    # - https://developers.google.com/drive/api/v3/push

    while True:
        time.sleep(60*60)
        sync_once(source, destination)
