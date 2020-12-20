import sys

from start_syncing import start_syncing
from stop_syncing import stop_syncing
from sync_once import sync_once

def main():
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
