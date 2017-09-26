#!/usr/bin/python
import subprocess
import sys
import time
import getpass

import ssh_cmd as ssh
import render_manager
import config

'''
Parent PID - Host - Client - Render Engine Path -
Render Files Path - Render Files - Log File - Render Arguments
'''
try:
    parent_pid = int(sys.argv[1])
    host = str(sys.argv[2])
    client = str(sys.argv[3])
    client_id = int(sys.argv[4])
    render_engine_path = str(sys.argv[5])
    log_file = str(sys.argv[6])
    render_arguments = str(sys.argv[7])
    render_files_path = str(sys.argv[8])
    render_files = sys.argv[9:]

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
    render_command = "{0} -f {1} {2}".format(render_engine_path,
                                             render_files_path + "/"
                                             + frame, "-V 2 0 0 1 0")
    ssh_connection.sendline(render_command)

ssh_connection.logout()

settings = config.Settings()
database_path = settings.render_database_file
render_db = render_manager.Database(database_path)
render_db.clean(client_id)
render_db.save_csv()

