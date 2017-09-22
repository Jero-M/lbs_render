#!/usr/bin/python
import subprocess
import sys
import time

'''
Parent PID - Host - Client - Render Engine Path -
Render Files Path - Render Files - Log File - Render Arguments
'''
try:
    parent_pid = str(sys.argv[1])
    host = str(sys.argv[2])
    client = str(sys.argv[3])
    render_engine_path = str(sys.argv[4])
    render_files_path = str(sys.argv[5])
    render_files = str(sys.argv[6])
    log_file = str(sys.argv[7])
    render_arguments = str(sys.argv[8])

except:
    parent_pid = 0
    host = None
    client = None
    render_engine_path  = None
    render_files_path = None
    render_files = None
    log_file = None
    render_arguments = None

print (parent_pid, host, client, render_engine_path,
      render_files_path, render_files, log_file, render_arguments)
time.sleep(2)

