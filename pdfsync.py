import os
import platform
import shutil
import subprocess
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
        print("pdfsync start [--foreground] <source> <destination>")
        print("pdfsync stop [--foreground] <source> <destination>")
        sys.exit(1)
    
    action = sys.argv[1]
    if action == "once":
        source, destination = sys.argv[2], sys.argv[3]
        sync_once(source, destination)
        print(f"Done! Synced '{source}' with '{destination}'")
    elif action == "start":
        if sys.argv[2] == "--foreground":
            source, destination = sys.argv[3], sys.argv[4]
            start_syncing(source, destination)
        else:
            source, destination = sys.argv[2], sys.argv[3]
            print(f"Starting background process to sync '{source}' with '{destination}'...")
            subprocess.Popen([sys.executable, __file__, "start", "--foreground", source, destination])
            sys.exit(0)
    elif action == "stop":
        if sys.argv[2] == "--foreground":
            source, destination = sys.argv[3], sys.argv[4]
            stop_syncing(source, destination)
        else:
            source, destination = sys.argv[2], sys.argv[3]
            print(f"Stopping background process to sync '{source}' with '{destination}'...")
            subprocess.Popen([sys.executable, __file__, "stop", "--foreground", source, destination])
            sys.exit(0)

if __name__ == "__main__":
    main()
