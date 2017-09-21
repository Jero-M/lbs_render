#!/usr/bin/python
import sys
import os
from PyQt4 import QtCore, QtGui
from qt_ui import Ui_renderTool
from os.path import isfile

import render_manager
import filecheck
import render


ui_colors = {"red":(150, 60, 60), "green":(60, 150, 69),
             "orange":(196, 99, 9), "grey":(140, 140, 140),
             "black":(76,76,76)}


class StartUI(QtGui.QMainWindow):
    '''Build an instance of the GUI'''

    def __init__(self, hostname, pid, database, default_dir, file_filters, parent=None):
        '''Initialize the interface with the correct settings'''
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_renderTool()
        self.ui.setupUi(self)
        self.watcher = QtCore.QFileSystemWatcher(self)

        #Default settings
        self.default_dir = default_dir
        self.file_filters = file_filters
        self.hostname = hostname
        self.pid = pid

        #Open the render database
        self.database_path = database
        self.render_db = render_manager.Database(self.database_path)

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

        #Automatically load the database
        self.watcher.addPath(self.database_path)
        self.create_tree_list()

    def create_tree_list(self):
        '''Create the QTreeWidgetItem for every row and store it in a
        dictionary'''
        self.render_db.open_csv(self.database_path)
        for row in self.render_db.data[1:]:
            tree_list = QtGui.QTreeWidgetItem(self.ui.render_list)
            self.render_list_ids.append(row[0])
            self.render_list_items[row[0]] = tree_list

            tree_list.setText(0, self.format_tree_items(row[1]))
            tree_list.setText(1, self.format_tree_items(row[2]))
            tree_list.setText(2, self.format_tree_items(row[3]))
            tree_list.setText(3, self.format_tree_items(row[4]))
            tree_list.setText(4, self.format_tree_items(row[5]))
            tree_list.setText(5, self.format_tree_items(row[6]))
            tree_list.setCheckState(6, QtCore.Qt.Unchecked)
            cancel_button = QtGui.QPushButton("Stop", self)
            cancel_button.setMinimumSize(QtCore.QSize(80, 20))
            cancel_button.setMaximumSize(QtCore.QSize(80, 20))
            self.ui.render_list.setItemWidget(tree_list, 7, cancel_button)
            self.tree_color_formatting(tree_list)

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
            self.tree_color_formatting(tree_list)

    def tree_color_formatting(self, row):
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
            #Uncheck select box
        elif status == "Available":
            self.change_text_color(row, 0, "black")
            self.change_text_color(row, 1, "green")
            self.change_text_color(row, 2, "black")
            self.change_text_color(row, 3, "black")
            self.change_text_color(row, 4, "black")
            self.change_text_color(row, 5, "black")
            row.setDisabled(False)
        elif status == "Rendering":
            self.change_text_color(row, 0, "grey")
            self.change_text_color(row, 1, "orange")
            self.change_text_color(row, 2, "grey")
            self.change_text_color(row, 3, "grey")
            self.change_text_color(row, 4, "grey")
            self.change_text_color(row, 5, "grey")
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

        #Divide frames per clients
        #Create a list based on input start frame, end frames and step
        frame_range = range(int(self.ui.start_frame_entry.text()),
                             int(self.ui.end_frame_entry.text()) + 1,
                             int(self.ui.steps_entry.text()))
        frames_per_client = render.assign_frames_to_clients(
                                                selected_clients_ids,
                                                frame_range,
                                                self.ifd_seq.filename_head,
                                                self.ifd_seq.seq_padding,
                                                self.ifd_seq.filename_tail)

        #Update Render Database
        self.render_db.open_csv(self.database_path)
        for client in selected_clients_ids:
            self.render_db.busy(client)
            self.render_db.set_host(client, self.hostname)
            self.render_db.set_ifd(client, file_entry)
            self.render_db.set_start_time(client, 1)
            self.render_db.set_progress(client, 0)
        # self.render_db.save_csv()
        #Start a new process for every client
        project_path = os.path.dirname(os.path.realpath(__file__)) + "/"
        selected_render = project_path + "mantra.py"
        
        for client in selected_clients_ids:
            client_name = self.render_db.get_client(client) + ".local"
            render.start_process(selected_render, self.pid, self.hostname,
                                 client_name, frames_per_client[client],
                                 "test.txt", 8)

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
    myapp = StartUI(node(), os.getpid(), settings.render_database_file,
                    settings.default_dir, settings.ifd_extensions)
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

