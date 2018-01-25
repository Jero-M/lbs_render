#!/usr/bin/python
import unittest
import sys
import os

test_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, test_path)

import render_manager
import config


class TestRenderDatabase(unittest.TestCase):
    '''Tests for the Render Manager Database'''

    def setUp(self):
        '''Create a database and modify it'''
        self.settings = config.Settings()
        self.database_path = self.settings.render_database_file
        self.default_id = [1, "comp-001", "Available", "None", "None", "None",
                           "None", "None"]
        self.header = ["id", "client", "status", "host", "ifd", "start_time",
                       "progress", "pids"]
        self.valid_status = ["Available", "Disabled", "Rendering"]

    def test_get_row(self):
        '''Test that a row has a length of 8'''
        row = render_manager.get_row(self.database_path, 1)
        self.assertEqual(len(row), 8)

    def test_get_client(self):
        '''Test that the client ID is a string'''
        client = render_manager.get_client(self.database_path, 4)
        self.assertIsInstance(client, str)

    def test_all_clients_are_valid(self):
        '''Test that all clients are in the all_clients db'''
        clients_from_config = self.settings.clients
        clients_from_db = render_manager.get_all_clients(self.database_path)
        self.assertListEqual(clients_from_db, clients_from_config)

    def test_get_available_clients(self):
        '''Test that all the available clients are returned'''
        render_manager.disable_all(self.database_path)
        render_manager.enable(self.database_path, 2)
        render_manager.enable(self.database_path, 4)
        render_manager.enable(self.database_path, 6)
        compare_to = [render_manager.get_client(self.database_path, 2),
                      render_manager.get_client(self.database_path, 4),
                      render_manager.get_client(self.database_path, 6)]
        available_clients = render_manager.get_available_clients(
                                                            self.database_path)
        self.assertListEqual(compare_to, available_clients)

    def test_get_status(self):
        '''Test that the status of a single client is valid'''
        self.assertIn(render_manager.get_status(self.database_path, 2),
                      self.valid_status)

    def test_all_status(self):
        '''Test that all the status of the clients are valid'''
        clients = render_manager.get_all_clients(self.database_path)
        for i, row in enumerate(clients):
            status = render_manager.get_status(self.database_path, i + 1)
            self.assertIn(status, self.valid_status)

    # def test_all_get_host(self):
    #     '''Test that a all hosts are valid'''
    #     clients = render_manager.get_all_clients(self.database_path)
    #     # clients.append("None")
    #     for i, row in enumerate(clients):
    #         host = render_manager.get_host(self.database_path, i + 1)
    #         self.assertIn(host, clients)

    def test_all_get_ifd(self):
        '''Test that all IFDs are a path or none'''
        clients = render_manager.get_all_clients(self.database_path)
        for i, row in enumerate(clients):
            ifd = render_manager.get_ifd(self.database_path, i + 1)
            if ifd == "None":
                self.assertEqual(ifd, "None")
            else:
                self.assertTrue(os.path.isfile(ifd))

    def test_disable(self):
        '''Test that a row is disabled'''
        render_manager.disable(self.database_path, 2)
        self.assertEqual(render_manager.get_status(self.database_path, 2),
                         "Disabled")

    def test_enable(self):
        '''Test that a row is enabled'''
        render_manager.enable(self.database_path, 5)
        self.assertEqual(render_manager.get_status(self.database_path, 5),
                         "Available")

    def test_busy(self):
        '''Test that a row is rendering'''
        render_manager.busy(self.database_path, 8)
        self.assertEqual(render_manager.get_status(self.database_path, 8),
                         "Rendering")

    def test_disable_all(self):
        '''Test that all clients are disabled'''
        clients = render_manager.get_all_clients(self.database_path)
        render_manager.disable_all(self.database_path)
        for i, row in enumerate(clients):
            status = render_manager.get_status(self.database_path, i + 1)
            self.assertEqual(status, "Disabled")

    def test_enable_all(self):
        '''Test that all clients are enabled'''
        clients = render_manager.get_all_clients(self.database_path)
        render_manager.enable_all(self.database_path)
        for i, row in enumerate(clients):
            status = render_manager.get_status(self.database_path, i + 1)
            self.assertEqual(status, "Available")

    def test_set_host(self):
        '''Test that the host is set'''
        render_manager.set_host(self.database_path, 2, "FXTD-001")
        self.assertEqual(render_manager.get_host(self.database_path, 2),
                         "FXTD-001")

    def test_set_ifd(self):
        '''Test that the ifd is set'''
        ifd_path = "/lbs/staff/hip/test.ifd"
        render_manager.set_ifd(self.database_path, 4, ifd_path)
        self.assertEqual(render_manager.get_ifd(self.database_path, 4),
                         ifd_path)
        render_manager.set_ifd(self.database_path, 4, "None")

    def test_set_start_time(self):
        '''Test that the start time is set'''
        render_manager.set_start_time(self.database_path, 10, 5.0)
        self.assertEqual(render_manager.get_start_time(self.database_path, 10),
                         "5.0")

    def test_add_pid(self):
        '''Test that a PID is appended to the list'''
        render_manager.add_pid(self.database_path, 4, 20)
        pids = render_manager.get_pids(self.database_path, 4)
        self.assertIn(20, pids)

    def test_add_multiple_pids(self):
        '''Test adding multiple PIDS'''
        render_manager.add_pid(self.database_path, 5, 21)
        render_manager.add_pid(self.database_path, 5, 22)
        render_manager.add_pid(self.database_path, 5, 23)
        pids = render_manager.get_pids(self.database_path, 5)
        self.assertEqual([21, 22, 23], pids)

    def test_remove_pid(self):
        '''Test that a PID is removed from the list'''
        render_manager.add_pid(self.database_path, 3, 31)
        render_manager.remove_pid(self.database_path, 3, 31)
        pids = render_manager.get_pids(self.database_path, 3)
        self.assertEqual(None, pids)

    def test_remove_single_pid(self):
        '''Test removing a single PID from a list of several'''
        render_manager.add_pid(self.database_path, 6, 31)
        render_manager.add_pid(self.database_path, 6, 32)
        render_manager.add_pid(self.database_path, 6, 33)
        render_manager.remove_pid(self.database_path, 6, 32)
        pids = render_manager.get_pids(self.database_path, 6)
        self.assertEqual([31, 33], pids)

    def test_clean(self):
        '''Test that clean will return a clean row'''
        client_id = 4
        render_manager.disable(self.database_path, client_id)
        render_manager.set_host(self.database_path, client_id, "FXTA-001")
        render_manager.set_ifd(self.database_path, client_id,
                               "/lbs/staff/hip/test.ifd")
        render_manager.set_start_time(self.database_path, client_id, 2.3)
        render_manager.set_progress(self.database_path, client_id, 0.1)
        render_manager.clean(self.database_path, client_id)
        self.assertEqual(render_manager.get_row(
                    self.database_path, client_id)[2:], self.default_id[2:])

    # def test_reset_to_defaults(self):
    #     '''Test that the database is reset to its defaults'''
    #     clients = render_manager.get_all_clients(self.database_path)
    #     render_manager.reset_to_defaults(self.database_path)
    #     for i, row in enumerate(clients):
    #         self.assertEqual(row[2:], self.default_id[2:])


unittest.main()