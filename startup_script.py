import json
import os
import sys

DATA_DIR = os.path.expanduser("~/.pdfsync")
STARTUP_FILE = os.path.join(DATA_DIR, "to_sync.json")

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
PDFSYNC = os.path.join(SCRIPT_DIR, "pdfsync.py")

def main():
    if not os.path.isfile(STARTUP_FILE):
        sys.exit(0)
    
    with open(STARTUP_FILE, "r", encoding="utf8") as file:
        to_sync = json.load(file)
    
    for source, destinations in to_sync.items():
        for destination in destinations:
            command = ' '.join([sys.executable, PDFSYNC, "start", f"'{source}'", f"'{destination}'"])
            print(f"Running: {command}")
            os.system(command) # Run the child process synchronously, pdfsync start|stop is already asynchronous

if __name__ == "__main__":
    main()
