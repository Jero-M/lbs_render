#!/usr/bin/python
import os
import csv
import getpass
import sys


class Settings(object):
    '''Create the settings'''
    main_path = os.path.dirname(os.path.realpath(__file__))
    default_config_file = "/etc/config"

    def __init__(self, config_file=""):
        '''Load the default settings from the config file'''
        if config_file == "":
            self.config_file = str(Settings.main_path
                               + Settings.default_config_file)
        else:
            self.config_file = config_file
        self.config_list = []
        self.open_config_file(self.config_file)
        self.user = getpass.getuser()
        self.clients_file = self.get_abs_path(self.load_setting("All Clients"))
        self.clients = self.load_clients(self.clients_file)
        self.student_mapping = self.load_student_mapping(self.clients_file)
        self.render_database_file = self.get_abs_path(
                                     self.load_setting("Render Database"))
        self.houdini_dir = self.get_abs_path(
                            self.load_setting("Houdini Install Directory"))
        self.houdini_versions = self.get_houdini_versions(
                                 self.load_setting("Houdini Versions"))
        self.mantra_path = self.get_mantra_path(self.load_setting("Mantra Path"),
                                                self.houdini_dir,
                                                sorted(self.houdini_versions.keys(),
                                                reverse=True)[0])
        self.render_client_ui = self.get_abs_path(
                                 self.load_setting("Render Client UI"))
        self.canceled_ui = self.get_abs_path(
                            self.load_setting("Canceled Render UI"))
        self.default_dir = self.get_default_dir(
                            self.load_setting("Default Directory"))
        self.ifd_extensions = self.get_ifd_extensions(
                               self.load_setting("IFD File Extensions"))
        self.compression = self.get_compression(self.ifd_extensions)
        self.debug_level = self.get_default_ui_values("Debug")
        self.ignore_host = self.get_default_ui_values("Ignore Host Username")
        self.default_steps = self.get_default_ui_values("Steps")
        self.default_processors = self.get_default_ui_values("Processors")
        self.default_verbose = self.get_default_ui_values("Verbose")
        self.default_vex_profiling = self.get_default_ui_values("VEX Profiling")
        self.default_nan_detection = self.get_default_ui_values("NAN Detection")
        self.default_alfred_style = self.get_default_ui_values("Alfred Style")
        self.default_time_stamps = self.get_default_ui_values("Time Stamps")
        self.default_verbosity_off = self.get_default_ui_values("Verbosity Off")
        self.default_delete_ifds = self.get_default_ui_values("Delete IFDs")

    def open_config_file(self, file_path):
        '''Open a config file and store every line as an element in a list'''
        self.config_file = file_path
        self.config_list = []
        try:
            with open(self.config_file, "rb") as config:
                self.config_list = config.readlines()
        except Exception as e:
            print ("Error loading the config file from file"
                  + "{0}. Error: {1}".format(file_path, e))

    def load_setting(self, setting_name):
        '''Load a single setting'''
        setting_value = None
        for row in self.config_list:
            if setting_name.lower() in row.lower():
                setting_value = row.split("=")[-1].strip()
                return setting_value
        return setting_value

    def load_clients(self, file_path):
        '''Load the clients.csv file into a list'''
        clients = []
        try:
            with open(file_path, "rb") as csv_file:
                reader = csv.reader(csv_file)
                for i, row in enumerate(reader):
                    if i == 0: continue
                    clients.append(row[0])
        except Exception as e:
            print ("Error loading the client list from file" +
                  + "{0}. Error: {1}".format(file_path, e))
            return clients
        else:
            return clients

    def load_student_mapping(self, file_path):
        '''Map the clients to the student names from the clients.csv file'''
        student_mapping = {}
        with open(file_path, "rb") as csv_file:
            reader = csv.reader(csv_file)
            for i, row in enumerate(reader):
                if i == 0: continue
                student_mapping[row[0]] = row[1]
        return student_mapping   

    def reload_files(self):
        '''Reload users, clients and mapping files'''
        self.clients_file = self.get_abs_path(self.load_setting("All Clients"))
        self.clients = self.load_clients(self.clients_file)
        self.student_mapping = self.load_student_mapping(self.clients_file)

    def get_houdini_versions(self, versions):
        '''Return a list with the path of the houdini versions'''
        version_list = {self.formatted_version(version.strip()):version.strip()
                        for version in versions.split(",")}
        return version_list

    def formatted_version(self, version):
        '''Remove hfs from the version name for nicer displaying'''
        return version.replace("hfs", "").strip()

    def get_default_dir(self, dir_path):
        '''Get the path to the default directory of the file dialog'''
        return dir_path.replace("$USER$", self.user)

    def get_mantra_path(self, path, hou_dir, hou_version):
        '''Return the path to Mantra from the current houdini version'''
        new_path = path.replace("$HOU_INSTALL$", hou_dir)
        new_path = new_path.replace("$HOU_VERSION$", hou_version)
        return new_path

    def get_ifd_extensions(self, filters):
        '''Return the properly formatted string of valid extensions for QT'''
        filter_string = ["*." + ext_filter.strip() for ext_filter in
                         filters.split(",")]
        return " ".join(filter_string)

    def get_compression(self, extensions):
        '''Return a list of valid compression extensions'''
        compression = [ext.partition(".")[-1] for ext in extensions.split(" ")
                      if "ifd" not in ext]
        return compression

    def get_default_ui_values(self, ui_setting):
        '''Return the default int value for the UI controls'''
        return int(self.load_setting(ui_setting))

    def get_abs_path(self, path):
        '''Return an absolute path from a relative path'''
        if path[0] == ".":
            return Settings.main_path + path[1:]
        else:
            return path


if __name__ == "__main__":
    project_path = os.path.dirname(os.path.realpath(__file__))
    settings= Settings()
    user = settings.user
    clients = settings.clients
    students_mapping = settings.student_mapping
    students_list = students_mapping.values()
    render_database = settings.render_database_file

    houdini_versions = settings.houdini_versions
    houdini_dir = settings.houdini_dir
    mantra_dir = settings.mantra_path

    print "CURRENT USER:", user, "\n-----------------------"
    print "CLIENT LIST:"
    for client in clients:
        print client
    print "-----------------------"
    print "STUDENTS MAPPING"
    for client in clients:
        try:
            print client + ":", students_mapping[client]
        except:
            print client
    print "-----------------------"
    print "RENDER DATABASE:", render_database
    print "-----------------------"
    print ("HOUDINI INSTALL DIRECTORY: " + houdini_dir
           + "\n-----------------------")
    print ("HOUDINI VERSIONS: " + ", ".join(houdini_versions)
           + "\n-----------------------")
    print "MANTRA PATH: " + mantra_dir + "\n-----------------------" 
    print "IFD EXTENSIONS:", settings.ifd_extensions 
    print "-----------------------"  
    print "IFD COMPRESSION:", settings.compression
    print "-----------------------"
    sys.exit()