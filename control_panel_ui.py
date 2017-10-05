#!/usr/bin/python
import sys
import os
import signal
from PyQt4 import QtCore, QtGui
from control_panel_qt_ui import Ui_renderTool
from os.path import isfile
from datetime import datetime

import render_manager
import filecheck
import render
import config


ui_colors = {"red":(150, 60, 60), "green":(60, 150, 69),
             "orange":(196, 99, 9), "grey":(140, 140, 140),
             "black":(76,76,76)}


class StartUI(QtGui.QMainWindow):
    '''Build an instance of the GUI'''

    def __init__(self, hostname, pid, parent=None):
        '''Initialize the interface with the correct settings'''
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_renderTool()
        self.ui.setupUi(self)
        self.watcher = QtCore.QFileSystemWatcher(self)

        #Default settings
        self.settings = config.Settings()
        self.default_dir = self.settings.default_dir
        self.file_filters = self.settings.ifd_extensions
        self.hostname = hostname
        self.pid = pid

        #Open the render database
        self.database_path = self.settings.render_database_file
        self.render_db = render_manager.Database(self.database_path)

        #IFD Sequence
        self.ifd_seq = ""

        #Render Processes IDs
        self.render_processes = {}

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
        self.watcher.addPath(self.database_path)
        self.create_tree_list()

    def create_tree_list(self):
        '''Create the QTreeWidgetItem for every row and store it in a
        dictionary'''
        self.render_db.open_csv(self.database_path)
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
        self.render_db.open_csv(self.database_path)
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
            if status == "Disabled" or status == "Rendering" and self.hostname != current_host:
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

    def file_dialog(self):
        '''Open a file dialog'''
        self.filename = QtGui.QFileDialog.getOpenFileName(self,
                        "Open IFD file", self.default_dir,
                        "IFD files ({0})".format(self.file_filters))
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
        render_engine_path = self.settings.get_mantra_path(
            self.settings.mantra_path,
            self.settings.houdini_dir,
            self.settings.houdini_versions[str(self.ui.version_list.currentText())])
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
        self.render_db.open_csv(self.database_path)
        for client in selected_clients_ids:
            self.render_db.busy(client)
            self.render_db.set_host(client, self.hostname)
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
            render_pid = render.start_process(self.pid,
                                              self.hostname,
                                              client_name,
                                              client,
                                              render_engine_script,
                                              render_engine_path,
                                              log_file,
                                              render_args,
                                              render_files_path,
                                              render_files,
                                             )
            self.render_processes[client] = render_pid

    def stop_render(self):
        '''Stop the current render'''
        target = self.sender()
        target_id = int(target.row_id)
        try:
            kill_pid = int(self.render_processes[target_id])
        except:
            print "Render process was not found"
            return
        # cancel_cmd = "kill -9 {0}".format(str(target_id))
        kill = os.kill(kill_pid, signal.SIGKILL)
        print kill_pid
        print kill
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
    import config
    from platform import node
    settings = config.Settings()
    app = QtGui.QApplication(sys.argv)
    myapp = StartUI(node(), os.getpid())
    myapp.show()
    myapp.set_versions(["16.0", "15.3.03"])
    myapp.set_start_frame(0)
    myapp.set_end_frame(20)
    myapp.set_steps(1)
    myapp.set_processors(0)
    myapp.set_verbose(2)
    myapp.set_message("Test")
    myapp.enable_vex_profiling(True)
    myapp.enable_nan_detection(True)
    myapp.enable_alfred_style(True)
    myapp.enable_time_stamps(True)
    myapp.enable_verbosity(True)
    myapp.enable_delete_ifd(True)
    test = myapp.get_all_settings()
    print test

    sys.exit(app.exec_())

