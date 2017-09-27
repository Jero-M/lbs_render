#!/usr/bin/python
import subprocess
import sys
import time
import getpass
import os

import ssh_cmd as ssh
import render_manager
import config

'''
Parent PID - Host - Client - Render Engine Path -
Render Files Path - Render Files - Log File - Render Arguments
'''
project_path = os.path.dirname(os.path.realpath(__file__))

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
    sys.exit()

settings = config.Settings()
database_path = settings.render_database_file

user = getpass.getuser()
ssh_connection = ssh.ssh_start(client, user)

for i, frame in enumerate(render_files):
    render_command = "{0} -f {1} {2}".format(render_engine_path,
                                             render_files_path + "/"
                                             + frame, "-V 2 0 0 1 0")
    update_render_db_command = "python {0}/render_manager.py {1} None None None None {2}/{3}".format(project_path, client_id, str(i + 1), str(len(render_files)))
    ssh.send_cmd(ssh_connection, render_command)
    print update_render_db_command
    ssh.send_cmd(ssh_connection, update_render_db_command)

ssh.ssh_close(ssh_connection)

render_db = render_manager.Database(database_path)
render_db.clean(client_id)
render_db.save_csv()