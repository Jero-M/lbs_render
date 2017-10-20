#!/usr/bin/python
import unittest
import sys
import os

test_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, test_path)

from render_manager import Database
import config

class TestRenderDatabase(unittest.TestCase):
    '''Tests for the Render Manager Database'''

    def setUp(self):
        '''Create a database and modify it'''
        self.settings = config.Settings()
        self.database_path = self.settings.render_database_file
        self.render_db = Database(self.database_path)
        self.default_id = [1, "comp-001", "Available", "None", "None", "None",
                           "None", "None"]
        self.header = ["id", "client", "status", "host", "ifd", "start_time",
                      "progress", "pids"]
        self.valid_status = ["Available", "Disabled", "Rendering"]

    def test_header_integrity(self):
        '''Test that the header is the same'''
        self.assertEqual(self.render_db.header, self.header)

    def test_get_row(self):
        '''Test that a row has a length of 7'''
        row = self.render_db.get_row(1)
        self.assertEqual(len(row), 8)

    def test_get_client(self):
        '''Test that the client ID is a string'''
        client = self.render_db.get_client(4)
        self.assertEqual(type(client), type("str"))

    def test_all_clients_are_valid(self):
        '''Test that all clients are in the all_clients db'''
        clients = self.settings.clients
        for i, row in enumerate(self.render_db.data):
            if i == 0: continue
            client = self.render_db.get_client(i)
            self.assertIn(client, clients)

    def test_get_available_clients(self):
        '''Test that all the available clients are returned'''
        self.render_db.disable_all()
        self.render_db.enable(2)
        self.render_db.enable(4)
        self.render_db.enable(6)
        compare_to = [self.render_db.get_client(2),
                      self.render_db.get_client(4),
                      self.render_db.get_client(6)]
        available_clients = self.render_db.get_available_clients()
        self.assertEqual(compare_to, available_clients)

    def test_get_status(self):
        '''Test that the status of a single client is valid'''
        self.assertIn(self.render_db.get_status(2), self.valid_status)

    def test_all_status(self):
        '''Test that all the status of the clients are valid'''
        clients = self.settings.clients
        for i, row in enumerate(self.render_db.data):
            if i == 0: continue
            status = self.render_db.get_status(i)
            self.assertIn(status, self.valid_status)

    def test_all_get_host(self):
        '''Test that a all hosts are valid'''
        clients = self.settings.clients
        clients.append("None")
        for i, row in enumerate(self.render_db.data):
            if i == 0: continue
            host = self.render_db.get_host(i)
            self.assertIn(host, clients)

    def test_all_get_ifd(self):
        '''Test that all IFDs are a path or none'''
        for i, row in enumerate(self.render_db.data):
            if i == 0: continue
            ifd = self.render_db.get_ifd(i)
            if ifd == "None": self.assertEqual(ifd, "None")
            else: self.assertTrue(os.path.isfile(ifd))

    def test_disable(self):
        '''Test that a row is disabled'''
        self.render_db.disable(2)
        self.assertEqual(self.render_db.get_status(2), "Disabled")

    def test_enable(self):
        '''Test that a row is enabled'''
        self.render_db.enable(5)
        self.assertEqual(self.render_db.get_status(5), "Available")

    def test_busy(self):
        '''Test that a row is rendering'''
        self.render_db.busy(8)
        self.assertEqual(self.render_db.get_status(8), "Rendering")

    def test_disable_all(self):
        '''Test that all clients are disabled'''
        self.render_db.disable_all()
        for i, row in enumerate(self.render_db.data):
            if i == 0: continue
            status = self.render_db.get_status(i)
            self.assertEqual(status, "Disabled")

    def test_enable_all(self):
        '''Test that all clients are enabled'''
        self.render_db.enable_all()
        for i, row in enumerate(self.render_db.data):
            if i == 0: continue
            status = self.render_db.get_status(i)
            self.assertEqual(status, "Available")

    def test_set_host(self):
        '''Test that the host is set'''
        self.render_db.set_host(2, "FXTD-001")
        self.assertEqual(self.render_db.get_host(2), "FXTD-001")

    def test_set_ifd(self):
        '''Test that the ifd is set'''
        ifd_path = "/lbs/staff/hip/test.ifd"
        self.render_db.set_ifd(4, ifd_path)
        self.assertEqual(self.render_db.get_ifd(4), ifd_path)

    def test_set_start_time(self):
        '''Test that the start time is set'''
        self.render_db.set_start_time(10, 5.0)
        self.assertEqual(self.render_db.get_start_time(10), 5.0)

    def test_set_start_time(self):
        '''Test that the progress is set'''
        self.render_db.set_progress(6, 0.5)
        self.assertEqual(self.render_db.get_progress(6), 0.5)

    def test_add_pid(self):
        '''Test that a PID is appended to the list'''
        self.render_db.add_pid(4, 20)
        pids = self.render_db.get_pids(4)
        self.assertIn(20, pids)

    def test_add_multiple_pids(self):
        '''Test adding multiple PIDS'''
        self.render_db.add_pid(5, 21)
        self.render_db.add_pid(5, 22)
        self.render_db.add_pid(5, 23)
        pids = self.render_db.get_pids(5)
        self.assertEqual([21, 22, 23], pids)

    def test_remove_pid(self):
        '''Test that a PID is removed from the list'''
        self.render_db.add_pid(3, 31)
        self.render_db.remove_pid(3, 31)
        pids = self.render_db.get_pids(3)
        self.assertEqual(None, pids)

    def test_remove_single_pid(self):
        '''Test removing a single PID from a list of several'''
        self.render_db.add_pid(6, 31)
        self.render_db.add_pid(6, 32)
        self.render_db.add_pid(6, 33)
        self.render_db.remove_pid(6, 32)
        pids = self.render_db.get_pids(6)
        self.assertEqual([31, 33], pids)

    def test_clean(self):
        '''Test that clean will return a clean row'''
        client_id = 4
        self.render_db.disable(client_id)
        self.render_db.set_host(client_id, "FXTA-001")
        self.render_db.set_ifd(client_id, "/lbs/staff/hip/test.ifd")
        self.render_db.set_start_time(client_id, 2.3)
        self.render_db.set_progress(client_id, 0.1)
        self.render_db.clean(client_id)
        self.assertEqual(self.render_db.get_row(client_id)[2:],
                         self.default_id[2:])

    def test_reset_to_defaults(self):
        '''Test that the database is reset to its defaults'''
        self.render_db.reset_to_defaults()
        for i, row in enumerate(self.render_db.data):
            if i == 0: continue
            self.assertEqual(row[2:], self.default_id[2:])


unittest.main()