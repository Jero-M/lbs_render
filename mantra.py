#!/usr/bin/python
import subprocess
import sys
import getpass
import os
import signal

import ssh_cmd as ssh
import render_manager
import config

'''
Parent PID - Host - Client - Render Engine Path -
Render Files Path - Render Files - Log File - Render Arguments
'''
project_path = os.path.dirname(os.path.realpath(__file__))
pID_instance = os.getpid()
parent_pID = os.getppid()


# Load system arguments
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


def sigterm_handler(signal, frame):
    ssh.ssh_close(ssh_connection)
    render_manager.clean(database_path, client_id)
    sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)


# If successful, load the settings
settings = config.Settings()
database_path = settings.render_database_file
user = getpass.getuser()

# Start SSH Connection with Client
ssh_connection = ssh.ssh_start(client, user)
child_pID = subprocess.check_output(["pgrep", "-P", str(pID_instance)])

# Add PID, Parent PID and SSH PID to database
render_manager.add_pid(database_path, client_id, pID_instance)
render_manager.add_pid(database_path, client_id, parent_pID)
render_manager.add_pid(database_path, client_id, child_pID)

# Send command for every frame
for i, frame in enumerate(render_files):
    render_command = "{0} -f {1} {2}".format(render_engine_path,
                                             render_files_path + "/" +
                                             frame, "-V 2 0 0 1 0")
    update_render_db_command = ("python {0}/render_manager.py {1}".format(
                                                                project_path,
                                                                client_id) +
                                " None None None None {0}/{1}".format(
                                                           i + 1,
                                                           len(render_files)))
    ssh.send_cmd(ssh_connection, update_render_db_command)
    ssh.send_cmd(ssh_connection, render_command)

# Close SSH Connection with Client
ssh.ssh_close(ssh_connection)

# Update the Render Database
render_manager.clean(database_path, client_id)
