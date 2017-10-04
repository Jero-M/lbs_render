#!/usr/bin/python
import os
import sys
from platform import node
from multiprocessing import cpu_count
from PyQt4 import QtCore, QtGui

import config
import control_panel_ui


def load_default_ui_settings(gui, settings):
    # Load the default UI settings from the config file
    gui.set_versions(sorted(settings.houdini_versions, reverse=True))
    gui.set_steps(settings.default_steps)
    gui.set_processors(settings.default_processors)
    gui.set_verbose(settings.default_verbose)
    gui.enable_vex_profiling(bool(settings.default_vex_profiling))
    gui.enable_nan_detection(bool(settings.default_nan_detection))
    gui.enable_alfred_style(bool(settings.default_alfred_style))
    gui.enable_time_stamps(bool(settings.default_time_stamps))
    gui.enable_verbosity(bool(settings.default_verbosity_off))
    gui.enable_delete_ifd(bool(settings.default_delete_ifds))


def main():
    # Initialize Main Variables
    project_path = os.path.dirname(os.path.realpath(__file__))
    settings = config.Settings()
    user = settings.user

    # System Variables
    hostname = node()
    pID_instance = os.getpid()
    cpus = cpu_count()

    #Error messages
    error_messages = {
                      0:"No Error",
                      1:"Invalid start frame",
                      2:"Invalid end frame",
                      3:"Invalid processors number",
                      4:"Invalid verbose level, use 0-9",
                      5:str("Invalid processors number, there's only "
                        + str(cpus) + " processors"),
                      6:"No IFD file selected",
                      7:"Invalid step number",
                      8:"Invalid client",
                      9:str("You can only render from your own computer. "
                       + "Render cancelled. Try again from your own computer"),
                     10:"IFD file does not exist",
                     }

    # Settings Variables
    ignore_host_name = settings.ignore_host

    # Clients
    clients = settings.clients
    students_list = settings.student_mapping

    # Houdini Varibles
    houdini_versions = settings.houdini_versions
    houdini_dir = settings.houdini_dir
    mantra_path = settings.mantra_path

    # Create the GUI
    application = QtGui.QApplication(sys.argv)
    gui = control_panel_ui.StartUI(hostname, pID_instance)
    load_default_ui_settings(gui, settings)

    # Show the GUI
    gui.show()
    # application.exec_()
    sys.exit(application.exec_())


if __name__ == "__main__":
    main()

'''
Priority List
1- Notify client of render
2- Turn UI controls into render arguments
3- Verbosity off should prevent terminal from opening
4- Uncheck selection for rendering so more renders can be sent
5- Stop button functionality
6- Delete IFD feature
7- Attach Message into render cmds
8- IFD File should be File and it should have %d04 instead of 0001
9- Progress bar

10- Client UI
11- Cancel through client side
12- Cancel UI
13- Notify host of cancelled render

14- Log module
15- Save in json format
16- Save every month in different directory

17- Config UI
18- Network Config UI

19- Arnold Support


Notify client? Run script that checks if db is changed. If its own hostname
is set to rendering, then run a command.


- Tree Widget Tasks -
1 - Time object
4 - Make Stop button call a function
5 - Disable Stop button based on host
6 - Disable Stop button if status is available
7 - Add frames list


- UI -
- Have errors display on a pop-up window

- Main -
1 - Errors
3 - Update script for clients.csv and render_clients
4 - Add ".local" in config
5 - Query selected render engine

- Render -
1 - Check for file integrity

- SSH -
1 - 

- Log Files -
1 - Write to json
2 - Organize by month

- Progress bar -

- Extra -
1 - Drag and drop

1- Click Render
    a- Render callback function
      i- Check if user is allowed to render
      ii- Check if IFD Exists
      iii- Gather selected clients
      iv- Divide frames per amount of clients
      v- Update render database to reserve clients
      vi- Start process for every client
      vii- SSH into client
      

- SSH Config -
- Get all network hosts and query their sshd_config
- Check if SSH Config has any allowed users. If it does, raise a warning
  - Give 2 options:
    - Ignore
    - Replace the SSH Config of the bad users for an allowed one
- Generate a known hosts file using every host
- Copy the known hosts to /etc/ssh/ssh_known_hosts in every network host
  - Having it in /etc/ makes it global for all users in the computer as opposed to having it in the users home dir
- Any changes made to the config of ssh inside /etc requires the ssh rervice to be restarted
  - sudo /etc/init.d/ssh restart
- Generate a pair of keys for every user
  - ssh-keygen -f /home/$user/.ssh/id_rsa -t rsa -N '' -C $user
    - -f is the output file, -t is the algorithm, -N is the passphrase (empty) and -C is the comment
  - This will save the keys in /home/.ssh as id_rsa.pub and id_rsa
- Create authorized keys by copying the pub key to the authorized_hosts inside .ssh
    - ssh-copy-id username@host
    - The contents of id_rsa.pub will be added to /home/.ssh/authorized_keys
- Double check file ownership and permissions are correct (That they aren't owned by root) Query using ls -la
  - /home/user chown user:users and chmod 700
  - ~/.ssh chown user:users and chmod 700
  - ~/.ssh/id_rsa chown user:users and chmod 600
  - ~/.ssh/id_rsa.pub chown user:users and chmod 700
  - ~/.ssh/authorized_keys chown user:users and chmod 600
- ssh-add might need to be used if an ssh-agent is already running but can't find keys attached
  - sign_and_send_pubkey: signing failed: agent refused operation
    - Query fingerprints using ssh-add -l
- Copy the authorized keys and private and public keys to every users /home/.ssh dir
- For debugging:
  - Use ssh -v user@host for verbosity
  - Check /var/log/auth.log in the remote computer for even more details
  - SSH with -X for display

On ~/.bashrc make sure you have:
  - ssh-add -D &> /dev/null
  - ssh-add &> /dev/null


- Network Config script
1- Start window with all IPs on a side and have option of editing, adding or removing
2- Query sshd_config in every IP and look for "allowed users"
  a- sshd_config is correct print "OK" message and proceed
  b- sshd_config has a few matches. Print them and give 2 options:
    i- Modify sshd_config scripts and remove "allowed users"
    ii- Ignore and continue
3- Generate ssh_known_hosts based on all IPs.
4- Copy ssh_known_hosts into every /etc/ on all IPs.
5- Restart ssh service for all IPs
6- Run "create_keys_per_user.sh"
7- Check if ssh-add is included in .bashrc of all home folders
  a- If it isnt add ssh-add into .bashrc
  b- Ignore

- Global Settings config


#!/bin/sh
export PYTHONPATH="/LOSTBOYS/LIBRARY/TECH_CONFIG/SOFTWARE/lbs_render/ext_modules"
python /LOSTBOYS/LIBRARY/TECH_CONFIG/SOFTWARE/lbs_render/main.py
exit


'''