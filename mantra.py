#!/usr/bin/python
import subprocess
import sys
import time
import getpass

import ssh_cmd as ssh

'''
Parent PID - Host - Client - Render Engine Path -
Render Files Path - Render Files - Log File - Render Arguments
'''
try:
    parent_pid = int(sys.argv[1])
    host = str(sys.argv[2])
    client = str(sys.argv[3])
    render_engine_path = str(sys.argv[4])
    log_file = str(sys.argv[5])
    render_arguments = str(sys.argv[6])
    render_files_path = str(sys.argv[7])
    render_files = sys.argv[8:]

except:
    # parent_pid = 0
    # host = None
    # client = None
    # render_engine_path  = None
    # render_files_path = None
    # render_files = None
    # log_file = None
    # render_arguments = None
    sys.exit()
# else:
    # sys.exit()

user = getpass.getuser()
ssh_connection = ssh.ssh_start(client, user)

for frame in render_files:
    render_command = "{0} -f {1} {2}".format(render_engine_path, frame, "-V 2 0 0 1 0")
    ssh_connection.sendline(render_command)

ssh_connection.logout()

# 1 - SSH Into client
# 2 - 

print (parent_pid, host, client, render_engine_path, log_file,
       render_arguments, render_files_path, render_files)
time.sleep(2)

