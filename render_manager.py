#!/usr/bin/python
import csv
import os
import sys

import config

class Database(object):
    '''Open a render_clients database csv and control it'''

    def __init__(self, file_path):
        '''Open the file and store the path, header and data'''
        self.path = file_path
        self.data = []
        self.header = []
        self.open_csv(self.path)

    def open_csv(self, file_path):
        '''Open a new csv file'''
        self.path = file_path
        self.data = []
        self.header = []
        with open(self.path, "rb") as csv_file:
            reader = csv.reader(csv_file)
            for i, row in enumerate(reader):
                if i == 0: self.header = row
                self.data.append(row)

    def save_csv(self):
        '''Save the data to the csv file'''
        with open(self.path, "wb") as csv_file:
            writer = csv.writer(csv_file)
            for row in self.data:
                writer.writerow(row)

    def reset_to_defaults(self):
        '''Reset every row to [id, client, "Availble", 0, 0, 0 ,0]'''
        for i, row in enumerate(self.data):
            if i == 0: continue
            self.clean(i)

    def disable_all(self):
        '''Disable all clients'''
        for i, row in enumerate(self.data):
            if i == 0: continue
            self.data[i][2] = "Disabled"

    def enable_all(self):
        '''Enable all clients'''
        for i, row in enumerate(self.data):
            if i == 0: continue
            self.data[i][2] = "Available"

    def get_available_clients(self):
        '''Return a list of all the available clients'''
        available_clients = []
        for i, row in enumerate(self.data):
            if i == 0: continue
            if row[2] == "Available": available_clients.append(row[1])
        return available_clients

    def get_row(self, id):
        '''Return a single row'''
        return self.data[id]

    def get_client(self, id):
        '''Return the client name of a row based on id'''
        return self.data[id][1]

    def get_status(self, id):
        '''Return the status of a row based on id'''
        return self.data[id][2]

    def get_host(self, id):
        '''Return the host name of a row based on id'''
        return self.data[id][3]

    def get_ifd(self, id):
        '''Return the ifd path of a row based on id'''
        return self.data[id][4]

    def get_start_time(self, id):
        '''Return the start time of a row based on id'''
        return float(self.data[id][5])

    def get_progress(self, id):
        '''Return the progress of a row based on id'''
        return float(self.data[id][6])

    def disable(self, id):
        '''Set status of a single client to Disabled'''
        if id == 0: return
        self.data[id][2] = "Disabled"

    def enable(self, id):
        '''Set status of a single client to Enabled'''
        if id == 0: return
        self.data[id][2] = "Available"

    def busy(self, id):
        '''Set status of a single client to Rendering'''
        if id == 0: return
        self.data[id][2] = "Rendering"

    def set_host(self, id, host_name):
        '''Set host name of a single client'''
        if id == 0: return
        assert type(host_name) == type("str")
        self.data[id][3] = host_name

    def set_ifd(self, id, ifd_path):
        '''Set the ifd path of single client'''
        if id == 0: return
        assert type(ifd_path) == type("str")
        self.data[id][4] = ifd_path

    def set_start_time(self, id, new_time):
        '''Set the start time of single client'''
        if id == 0: return
        self.data[id][5] = new_time

    def set_progress(self, id, new_progress):
        '''Set the progress of single client'''
        if id == 0: return
        self.data[id][6] = new_progress

    def clean(self, id):
        '''Reset a single row'''
        if id == 0: return
        self.data[id][2] = "Available"
        self.data[id][3] = "None"
        self.data[id][4] = "None"
        self.data[id][5] = "None"
        self.data[id][6] = "None"


if __name__ == "__main__":
    settings = config.Settings()
    database_path = settings.render_database_file

    try:
        client_id = int(sys.argv[1])
        status = sys.argv[2]
        host = sys.argv[3]
        file = sys.argv[4]
        time = sys.argv[5]
        progress = sys.argv[6]

        render_db = Database(database_path)
        if status != "None":
            if status == "Available":
                render_db.enable(client_id)
            elif status == "Rendering":
                render_db.busy(client_id)
            else:
                render_db.disable(client_id)

        if host != "None":
            render_db.set_host(client_id, host)
        if file != "None":
            render_db.set_ifd(client_id, file)
        if time != "None":
            render_db.set_start_time(client_id, time)
        if progress != "None":
            render_db.set_progress(client_id, progress)
        render_db.save_csv()

    except:
        test_db = Database(database_path)
        #Uncomment for resetting database
        # test_db.reset_to_defaults()
        # test_db.save_csv()
        print database_path
        print test_db.data
        print test_db.header

    sys.exit()