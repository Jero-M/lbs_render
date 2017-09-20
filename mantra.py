#!/usr/bin/python
import subprocess
import sys
import time

#Parent PID - Host - Client - mantra_path - render_list - log_file - processors
try:
    parent_id = str(sys.arg[1])
    host = str(sys.arg[2])
    client = str(sys.arg[3])
    mantra_path = str(sys.arg[4])
    render_list = str(sys.arg[5])
    log_file = str(sys.arg[6])
    processors = str(sys.arg[7])

except:
    parent_id = 0
    host = None
    client = None
    mantra_path = None
    render_list = None
    log_file = None
    processors = 0


time.sleep(5)
print parent_id, host, client, mantra_path, render_list, log_file, processors
