#!/usr/bin/python
import unittest
import sys
import os
import csv

test_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, test_path)

import config

config_data = ["All Clients = ./etc/clients.csv",
               "Render Database = ./database/render_clients.csv",
               "Houdini Install Directory = /LOSTBOYS/LIBRARY/TECH_CONFIG/SOFTWARE",
               "Houdini Versions = hfs16.0, hfs15.0.313",
               "Mantra Path = $HOU_INSTALL$/$HOU_VERSION$/bin/mantra",
               "Render Client UI = ./render_client_ui.py",
               "Canceled Render UI = ./canceled_render_ui.py",
               "Default Directory = /LOSTBOYS/FX/STUDENTS",
               "IFD File Extensions = ifd, gz, sc",
               "Debug = 0",
               "Ignore Host Username = 1",
               "Steps = 1",
               "Processors = 0",
               "Verbose = 2",
               "VEX Profiling = 0",
               "NAN Detection = 0",
               "Alfred Style = 1",
               "Time Stamps = 0",
               "Verbosity Off = 0",
               "Delete IFDs = 1",
              ]

class TestConfig(unittest.TestCase):
    '''Test the config module'''

    def setUp(self):
        '''Load the settings'''
        self.settings = config.Settings()

    def test_config_file(self):
        '''Test the location of the config file'''
        self.assertEqual(test_path + "/etc/config", self.settings.config_file)

    def test_config_list(self):
        '''Test that the config file contents match the config file'''
        contents = []
        with open(self.settings.config_file, "rb") as config:
            contents = config.readlines()
        self.assertEqual(contents, self.settings.config_list)

    def test_open_modified_config_file(self):
        '''Test loading a test config file and test if values update'''
        contents = []
        self.settings.open_config_file(test_path + "/tests/config_file_test")
        with open(self.settings.config_file, "rb") as config:
            contents = config.readlines()
        self.assertEqual(contents, self.settings.config_list)

    def test_clients_file(self):
        '''Test the clients file is valid'''
        path = test_path + "/etc/clients.csv"
        self.assertEqual(path, self.settings.clients_file)

    def test_clients_file_exists(self):
        '''Test the client file exists'''
        self.assertTrue(os.path.isfile(self.settings.clients_file))

    def test_clients(self):
        '''Test the clients match the clients from the file'''
        clients = []
        with open(test_path + "/etc/clients.csv", "rb") as csv_file:
            reader = csv.reader(csv_file)
            for i, row in enumerate(reader):
                if i == 0: continue
                clients.append(row[0])
        self.assertEqual(clients, self.settings.clients)

    def test_student_mapping(self):
        '''Test the student mappig match the mapping from the file'''
        mapping = {}
        with open(test_path + "/etc/clients.csv", "rb") as csv_file:
            reader = csv.reader(csv_file)
            for i, row in enumerate(reader):
                if i == 0: continue
                mapping[row[0]] = row[1]
        self.assertEqual(mapping, self.settings.student_mapping)

    def test_render_database_file(self):
        '''Test the render database file is valid'''
        path = test_path + "/database/render_clients.csv"
        self.assertEqual(path, self.settings.render_database_file)

    def test_render_database_file_exists(self):
        '''Test the client file exists'''
        self.assertTrue(os.path.isfile(self.settings.render_database_file))

    def test_houdini_dir(self):
        '''Test the houdini dir is valid'''
        path = "/LOSTBOYS/LIBRARY/TECH_CONFIG/SOFTWARE"
        self.assertEqual(path, self.settings.houdini_dir)

    def test_houdini_versions(self):
        '''Test the houdini versions'''
        versions = ["hfs16.0", "hfs15.0.313"]
        for version in versions:
            self.assertIn(version, self.settings.houdini_versions)

    def test_get_formatted_versions(self):
        '''Test if the versions are formatted nicely for printing'''
        formatted_versions = ["16.0", "15.0.313"]
        self.assertEqual(formatted_versions, self.settings.formatted_versions(
                                              self.settings.houdini_versions))

    def test_mantra_path(self):
        '''Test the mantra path is valid'''
        path = "/LOSTBOYS/LIBRARY/TECH_CONFIG/SOFTWARE/$HOU_VERSION$/bin/mantra"
        self.assertEqual(path, self.settings.mantra_path)

    def test_mantra_paths_exist(self):
        '''Test that the Mantra path exists for every version'''
        for version in self.settings.houdini_versions:
            self.assertTrue(os.path.isfile(
                            self.settings.mantra_path.replace("$HOU_VERSION$",
                                                              version)))

    def test_render_client_ui(self):
        '''Test the render client ui location is valid'''
        path = test_path + "/render_client_ui.py"
        self.assertEqual(path, self.settings.render_client_ui)

    def test_canceled_ui(self):
        '''Test the canceled ui location is valid'''
        path = test_path + "/canceled_render_ui.py"
        self.assertEqual(path, self.settings.canceled_ui)

    def test_default_dir(self):
        '''Test the default directory is valid'''
        path = "/LOSTBOYS/FX/STUDENTS"
        self.assertEqual(path, self.settings.default_dir)

    def test_default_dir_exists(self):
        '''Test the default directory file exists'''
        self.assertTrue(os.path.isdir(self.settings.default_dir))

    def test_ifd_extensions(self):
        '''Test the ifd extensions are valid'''
        extensions = "*.ifd *.gz *.sc"
        self.assertEqual(extensions, self.settings.ifd_extensions)

    def test_ifd_compression(self):
        '''Test the compressions are valid'''
        extensions = ["gz", "sc"]
        self.assertEqual(extensions, self.settings.compression)

    def test_reload_file(self):
        '''Test if reloading the config file reloads the file paths'''
        self.settings.open_config_file(test_path + "/tests/config_file_test")
        self.settings.reload_files()
        self.assertEqual(self.settings.clients_file, test_path
                         + "/tests/clients_file_test.csv")

    def test_reload_clients(self):
        '''Test if reloading clients updates the clients list'''
        self.settings.open_config_file(test_path + "/tests/config_file_test")
        self.settings.reload_files()
        clients = []
        with open(test_path
                  + "/tests/clients_file_test.csv", "rb") as csv_file:
            reader = csv.reader(csv_file)
            for i, row in enumerate(reader):
                if i == 0: continue
                clients.append(row[0])
        self.assertEqual(clients, self.settings.clients)

    def test_student_mapping(self):
        '''Test if reloading the mappings updates the mapping dictionary'''
        self.settings.open_config_file(test_path + "/tests/config_file_test")
        self.settings.reload_files()
        mapping = {}
        with open(test_path
                  + "/tests/clients_file_test.csv", "rb") as csv_file:
            reader = csv.reader(csv_file)
            for i, row in enumerate(reader):
                if i == 0: continue
                mapping[row[0]] = row[1]
        self.assertEqual(mapping, self.settings.student_mapping)


unittest.main()