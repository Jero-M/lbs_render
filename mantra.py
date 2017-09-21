#!/usr/bin/python
import subprocess
import sys
import time

#Parent PID - Host - Client - mantra_path - render_list - log_file - processors
print sys.argv[1]
print sys.argv[5]
print sys.argv[6]
print sys.argv[7]
try:
    parent_id = str(sys.argv[1])
    host = str(sys.argv[2])
    client = str(sys.argv[3])
    mantra_path = str(sys.argv[4])
    render_list = str(sys.argv[5])
    log_file = str(sys.argv[6])
    processors = str(sys.argv[7])

except:
    parent_id = 0
    host = None
    client = None
    mantra_path = None
    render_list = None
    log_file = None
    processors = 0

print parent_id, host, client, mantra_path, render_list, log_file, processors
time.sleep(2)

