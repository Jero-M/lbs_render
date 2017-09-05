#!/usr/bin/python
import os
import sys
from platform import node
from multiprocessing import cpu_count
from PyQt4 import QtCore, QtGui

import config
import ui


def load_default_ui_settings(gui, settings):
    # Load the default UI settings from the config file
    gui.set_versions(settings.formatted_versions(settings.houdini_versions))
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
    default_fd_dir = settings.default_dir
    ignore_host_name = settings.ignore_host
    file_filters = settings.ifd_extensions

    # Clients
    clients = settings.clients
    students_list = settings.student_mapping

    # Houdini Varibles
    houdini_versions = settings.houdini_versions
    houdini_dir = settings.houdini_dir
    mantra_path = settings.mantra_path

    # Create the GUI
    application = QtGui.QApplication(sys.argv)
    gui = ui.StartUI(default_fd_dir, file_filters)
    load_default_ui_settings(gui, settings)

    # Show the GUI
    gui.show()
    application.exec_()


if __name__ == "__main__":
    main()


'''
- Tree Widget Tasks -
1 - Time object
3 - Query Select checkbox
4 - Make Stop button call a function
5 - Disable Stop button based on host
6 - Disable Stop button if status is available

- UI -


- Main -
1 - Errors
2 - Uploading config file updates everything

- IFD File Entry -
1 - Event call when entry is changed
2 - Get IFD info (user, length, etc)

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
'''