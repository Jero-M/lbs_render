#!/usr/bin/python
import os
import sys
import signal
from platform import node
from os.path import isfile
from datetime import datetime
from multiprocessing import cpu_count


from PyQt4 import QtCore, QtGui
from control_panel_ui import Ui_renderTool

import config
import render_manager
import filecheck
import render


ui_colors = {"red":(150, 60, 60), "green":(60, 150, 69),
             "orange":(196, 99, 9), "grey":(140, 140, 140),
             "black":(76,76,76)}


class StartUI(QtGui.QMainWindow):
    '''Build an instance of the GUI'''

    def __init__(self, parent=None):
        '''Initialize the interface with the correct settings'''
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_renderTool()
        self.ui.setupUi(self)
        self.watcher = QtCore.QFileSystemWatcher(self)
        self.load_default_ui_settings()

        #Start the render database
        self.render_db = render_manager.Database(settings.render_database_file)

        #IFD Sequence
        self.ifd_seq = ""

        #Set tree columns width
        self.ui.render_list.setColumnWidth(0,115)
        self.ui.render_list.setColumnWidth(1,90)
        self.ui.render_list.setColumnWidth(2,120)
        self.ui.render_list.setColumnWidth(3,120)
        self.ui.render_list.setColumnWidth(4,80)
        self.ui.render_list.setColumnWidth(5,70)
        self.ui.render_list.setColumnWidth(6,60)
        self.ui.render_list.setColumnWidth(7,60)
        self.render_list_items = {}
        self.render_list_ids = []
        self.stop_buttons = {}

        #Signal Handling
        QtCore.QObject.connect(self.ui.browse_button,
                               QtCore.SIGNAL("clicked()"),
                               self.file_dialog)
        QtCore.QObject.connect(self.ui.render_button,
                               QtCore.SIGNAL("clicked()"),
                               self.gather_render_data)
        QtCore.QObject.connect(self.watcher,
                               QtCore.SIGNAL("fileChanged(const QString&)"),
                               self.update_tree_list)
        QtCore.QObject.connect(self.ui.file_path_entry,
                               QtCore.SIGNAL("textChanged(const QString&)"),
                               self.verify_file_input)
        QtCore.QObject.connect(self.ui.file_path_entry,
                               QtCore.SIGNAL("textChanged(const QString&)"),
                               self.verify_file_input)

        #Automatically load the database
        self.watcher.addPath(settings.render_database_file)
        self.create_tree_list()

    def create_tree_list(self):
        '''Create the QTreeWidgetItem for every row and store it in a
        dictionary'''
        self.render_db.open_csv(settings.render_database_file)
        for row in self.render_db.data[1:]:
            #Create tree list
            tree_list = QtGui.QTreeWidgetItem(self.ui.render_list)
            self.render_list_ids.append(row[0])
            self.render_list_items[row[0]] = tree_list

            #Set every coulmns text
            tree_list.setText(0, self.format_tree_items(row[1]))
            tree_list.setText(1, self.format_tree_items(row[2]))
            tree_list.setText(2, self.format_tree_items(row[3]))
            tree_list.setText(3, self.format_tree_items(row[4]))
            tree_list.setText(4, self.format_tree_items(row[5]))
            tree_list.setText(5, self.format_tree_items(row[6]))
            tree_list.setCheckState(6, QtCore.Qt.Unchecked)
            #Create stop button
            stop_button = QtGui.QPushButton("Stop", self)
            #Store row ID into the stop button
            stop_button.row_id = row[0]
            #Group all buttons in a dictionary
            self.stop_buttons[row[0]] = stop_button
            #Button size
            stop_button.setMinimumSize(QtCore.QSize(80, 20))
            stop_button.setMaximumSize(QtCore.QSize(80, 20))
            self.ui.render_list.setItemWidget(tree_list, 7, stop_button)
            #Connect button to function
            stop_button.clicked.connect(self.stop_render)
            #Fromat text
            self.tree_color_formatting(tree_list, row[0])

    def update_tree_list(self):
        '''Update the database by accessing the QTreeWidgetItem objects and
        editing the text''' 
        self.render_db.open_csv(settings.render_database_file)
        for row in self.render_db.data[1:]:
            tree_list = self.render_list_items[row[0]]
            tree_list.setText(0, self.format_tree_items(row[1]))
            tree_list.setText(1, self.format_tree_items(row[2]))
            tree_list.setText(2, self.format_tree_items(row[3]))
            tree_list.setText(3, self.format_tree_items(row[4]))
            tree_list.setText(4, self.format_tree_items(row[5]))
            tree_list.setText(5, self.format_tree_items(row[6]))
            status = tree_list.text(1)
            current_host = str(tree_list.text(2))
            if status == "Disabled" or status == "Rendering" and user + "@" + hostname != current_host:
                tree_list.setCheckState(6, QtCore.Qt.Unchecked)
            self.tree_color_formatting(tree_list, row[0])

    def tree_color_formatting(self, row, id):
        '''Format the interface of the tree view depending on its values'''
        status = str(row.text(1))
        if status == "Disabled":
            self.change_text_color(row, 0, "grey")
            self.change_text_color(row, 1, "red")
            self.change_text_color(row, 2, "grey")
            self.change_text_color(row, 3, "grey")
            self.change_text_color(row, 4, "grey")
            self.change_text_color(row, 5, "grey")
            row.setDisabled(True)
            self.stop_buttons[id].setEnabled(False)
            #Uncheck select box
        elif status == "Available":
            self.change_text_color(row, 0, "black")
            self.change_text_color(row, 1, "green")
            self.change_text_color(row, 2, "black")
            self.change_text_color(row, 3, "black")
            self.change_text_color(row, 4, "black")
            self.change_text_color(row, 5, "black")
            self.stop_buttons[id].setEnabled(False)
            row.setDisabled(False)
        elif status == "Rendering":
            self.change_text_color(row, 0, "grey")
            self.change_text_color(row, 1, "orange")
            self.change_text_color(row, 2, "grey")
            self.change_text_color(row, 3, "grey")
            self.change_text_color(row, 4, "grey")
            self.change_text_color(row, 5, "grey")
            self.stop_buttons[id].setEnabled(True)
            row.setDisabled(True)

    def format_tree_items(self, item):
        '''Format tree items text for nice display'''
        if type(item) == type("str"):
            if item == "None" or item == "0":
                return ""
            else:
                return item

    def change_text_color(self, row, column, color):
        '''Change the text color of the items in a Tree Widget'''
        row.setTextColor(column, QtGui.QColor(ui_colors[color][0],
                         ui_colors[color][1], ui_colors[color][2]))

    def load_default_ui_settings(self):
        '''Load the default UI settings from the config file'''
        self.set_versions(sorted(settings.houdini_versions, reverse=True))
        self.set_steps(settings.default_steps)
        self.set_processors(settings.default_processors)
        self.set_verbose(settings.default_verbose)
        self.enable_vex_profiling(bool(settings.default_vex_profiling))
        self.enable_nan_detection(bool(settings.default_nan_detection))
        self.enable_alfred_style(bool(settings.default_alfred_style))
        self.enable_time_stamps(bool(settings.default_time_stamps))
        self.enable_verbosity(bool(settings.default_verbosity_off))
        self.enable_delete_ifd(bool(settings.default_delete_ifds))

    def file_dialog(self):
        '''Open a file dialog'''
        self.filename = QtGui.QFileDialog.getOpenFileName(self,
                        "Open IFD file", settings.default_dir,
                        "IFD files ({0})".format(settings.ifd_extensions))
        if isfile(self.filename):
            self.ui.file_path_entry.setText(self.filename)

    def verify_file_input(self):
        '''Check if file exists, run filecheck and update UI'''
        file_entry = str(self.ui.file_path_entry.text())
        if not os.path.isfile(file_entry):
            self.disable_render()
            print "File does not exist"
            return
        self.ifd_seq = filecheck.RenderFile(file_entry)
        self.set_start_frame(self.ifd_seq.start_frame)
        self.set_end_frame(self.ifd_seq.end_frame)
        self.enable_render()

    def gather_render_data(self):
        '''Gather all the data from the UI and if valid begin rendering'''
        #Check if user is allowed
        #Check if IFD exists
        file_entry = str(self.ui.file_path_entry.text())
        if not os.path.isfile(file_entry):
            self.disable_render()
            print "File does not exist"
            return
        #Gather selected clients
        selected_clients_ids = [int(entry) for entry in self.render_list_ids
                               if self.render_list_items[entry].checkState(6)]
        #If no clients were selected then return
        if len(selected_clients_ids) == 0:
            print "No clients selected"
            return
        #Gather Render Data
        project_path = os.path.dirname(os.path.realpath(__file__)) + "/"
        render_engine_script = project_path + "mantra.py"
        render_engine_path = settings.get_mantra_path(
            settings.mantra_path,
            settings.houdini_dir,
            settings.houdini_versions[str(self.ui.version_list.currentText())])
        render_files_path = self.ifd_seq.directory
        log_file = "text.txt"
        render_args = "-v"

        #Divide frames per clients
        #Create a list based on input start frame, end frames and step
        frame_range = range(int(self.ui.start_frame_entry.text()),
                             int(self.ui.end_frame_entry.text()) + 1,
                             int(self.ui.steps_entry.text()))
        frames_seq = render.map_frames_to_files(frame_range,
                                                self.ifd_seq.filename_head,
                                                self.ifd_seq.seq_padding,
                                                self.ifd_seq.filename_tail)
        frames_per_client = render.assign_frames_to_clients(
                                                selected_clients_ids,
                                                frame_range)
        #Update Render Database
        self.render_db.open_csv(settings.render_database_file)
        for client in selected_clients_ids:
            self.render_db.busy(client)
            self.render_db.set_host(client, user + "@" + hostname)
            self.render_db.set_ifd(client, file_entry)
            self.render_db.set_start_time(client, datetime.today().strftime(
                                                         "%d.%m.%y %H:%M:%S"))
            self.render_db.set_progress(client, "0/{0}".format(str(len(
                                                 frames_per_client[client]))))
        self.render_db.save_csv()

        #Start a new process for every client
        for client in selected_clients_ids:
            client_name = self.render_db.get_client(client) + ".local"
            render_files = [frames_seq[render_file] for render_file in
                                                    frames_per_client[client]]
            render_pid = render.start_process(pID_instance,
                                              hostname,
                                              client_name,
                                              client,
                                              render_engine_script,
                                              render_engine_path,
                                              log_file,
                                              render_args,
                                              render_files_path,
                                              render_files,
                                             )
            # Set the Gnome-terminal PID in the database
            self.render_db.open_csv(settings.render_database_file)
            self.render_db.add_pid(client, render_pid)
            self.render_db.save_csv()

    def stop_render(self):
        '''Stop the current render'''
        target = self.sender()
        target_id = int(target.row_id)
        self.render_db.open_csv(settings.render_database_file)
        child_processes = self.render_db.get_pids(target_id)

        #Stop the local process that is sending the renders
        if child_processes != None:
            for process in child_processes:
                try:
                    os.kill(process, signal.SIGTERM)
                except:
                    continue

        #Stop the remote mantrabin process

            self.render_db.open_csv(settings.render_database_file)
            self.render_db.clean(target_id)
            self.render_db.save_csv()




        # try:
        #     kill_pid = int(self.render_processes[target_id])
        # except:
        #     print "Render process was not found"
        #     return
        # cancel_cmd = "kill -9 {0}".format(str(target_id))
        # os.killpg(3433, signal.SIGKILL)
        # kill = os.kill(kill_pid, signal.SIGKILL)
        # print kill_pid
        # print kill
        # if kill:
        #     return
        # else:
        #     print "Error cancelling the render"
        #     return

    def enable_render(self):
        '''Enable the render button'''
        self.ui.render_button.setEnabled(True)

    def disable_render(self):
        '''Disable the render button'''
        self.ui.render_button.setEnabled(False)

    def set_versions(self, versions):
        '''Add the versions into the QComboBox'''
        for version in versions:
            self.ui.version_list.addItem(version)

    def set_start_frame(self, frame):
        '''Set the start frame'''
        self.ui.start_frame_entry.setText(str(frame))

    def set_end_frame(self, frame):
        '''Set the end frame'''
        self.ui.end_frame_entry.setText(str(frame))

    def set_steps(self, step):
        '''Set the steps'''
        self.ui.steps_entry.setText(str(step))        

    def set_processors(self, amount):
        '''Set the amount of processors'''
        self.ui.processors_entry.setText(str(amount))  

    def set_verbose(self, level):
        '''Set the verbosity level'''
        self.ui.verbose_entry.setText(str(level))  

    def enable_vex_profiling(self, flag):
        '''Enable or disable vex profiling'''
        self.ui.verbose_vex_checkbox.setChecked(flag)

    def enable_nan_detection(self, flag):
        '''Enable or disable nan detection'''
        self.ui.verbose_nan_checkbox.setChecked(flag)

    def enable_alfred_style(self, flag):
        '''Enable or disable alfred style'''
        self.ui.verbose_alfred_checkbox.setChecked(flag)

    def enable_time_stamps(self, flag):
        '''Enable or diable time stamps'''
        self.ui.verbose_time_checkbox.setChecked(flag)

    def enable_verbosity(self, flag):
        '''Enable or disable verbosity'''
        self.ui.verbosity_off_checkbox.setChecked(flag)

    def enable_delete_ifd(self, flag):
        '''Enable or disable delete ifds after rendering'''
        self.ui.delete_ifd_checkbox.setChecked(flag)

    def set_message(self, message):
        '''Set a message on the message entry'''
        self.ui.message_entry.setText(str(message))

    def get_all_settings(self):
        ifd_settings = []
        ifd_settings.append(str(self.ui.file_path_entry.text()))
        ifd_settings.append(str(self.ui.version_list.currentText()))
        ifd_settings.append(str(self.ui.start_frame_entry.text()))
        ifd_settings.append(str(self.ui.end_frame_entry.text()))
        ifd_settings.append(str(self.ui.steps_entry.text()))
        ifd_settings.append(str(self.ui.processors_entry.text()))
        ifd_settings.append(str(self.ui.verbose_entry.text()))
        ifd_settings.append(self.ui.verbose_vex_checkbox.isChecked())
        ifd_settings.append(self.ui.verbose_nan_checkbox.isChecked())
        ifd_settings.append(self.ui.verbose_alfred_checkbox.isChecked())
        ifd_settings.append(self.ui.verbose_time_checkbox.isChecked())
        ifd_settings.append(self.ui.verbosity_off_checkbox.isChecked())
        ifd_settings.append(self.ui.delete_ifd_checkbox.isChecked())
        ifd_settings.append(str(self.ui.message_entry.text()))
        return ifd_settings


if __name__ == "__main__":
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

    # Create the GUI
    app = QtGui.QApplication(sys.argv)
    gui = StartUI()

    # Show the GUI
    gui.show()
    sys.exit(app.exec_())

'''
Priority List
0- Stop button functionality
1- Store PID of every render in the render_database
1b- Opening the Control Panel should load the render_processes PIDs from the render_database
3- Notify client of render
4- Turn UI controls into render arguments
5- Verbosity off should prevent terminal from opening
6- Uncheck selection for rendering so more renders can be sent

7- Delete IFD feature
8- Attach Message into render cmds
9- IFD File should be File and it should have %d04 instead of 0001
10- Progress bar

11- Client UI
12- Cancel through client side
13- Cancel UI
14- Notify host of cancelled render

15- Log module
16- Save in json format
17- Save every month in different directory

18- Config UI
19- Network Config UI

20- Arnold Support


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