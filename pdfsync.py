import os
import platform
import shutil
import sys

from start_syncing import start_syncing
from stop_syncing import stop_syncing
from sync_once import sync_once

WIN_STARTUP_DIR = os.path.expanduser("~/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup")
WIN_STARTUP_SCRIPT = os.path.join(WIN_STARTUP_DIR, "startup_script.py")
WIN_STARTUP_SCRIPT_CMD = os.path.join(WIN_STARTUP_DIR, "startup_script.cmd")

def add_startup_script():
    if platform.system() == 'Windows':
        os.makedirs(WIN_STARTUP_DIR, exist_ok=True)
        if not os.path.isfile(WIN_STARTUP_SCRIPT):
            shutil.copyfile("startup_script.py", WIN_STARTUP_SCRIPT)
        if not os.path.isfile(WIN_STARTUP_SCRIPT_CMD):
            with open(WIN_STARTUP_SCRIPT_CMD, "w", encoding="utf8") as file:
                file.write(f"{sys.executable} startup_script.py %*")
    # TODO: other OSes

def main():
    add_startup_script()

    if len(sys.argv) < 4:
        print("usage: pdfsync <once|start|stop> <args>")
        print("pdfsync once <source> <destination>")
        print("pdfsync start <source> <destination>")
        print("pdfsync stop <source> <destination>")
        sys.exit(1)
    
    action = sys.argv[1]
    source, destination = sys.argv[2], sys.argv[3]
    if action == "once":
        sync_once(source, destination)
    elif action == "start":
        start_syncing(source, destination) # TODO: in the background
    elif action == "stop":
        stop_syncing(source, destination) # TODO: in the background

if __name__ == "__main__":
    main()
