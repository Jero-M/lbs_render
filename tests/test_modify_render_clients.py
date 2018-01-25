#!/usr/bin/python
import os
import time
import sys

test_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, test_path)

from render_manager import Database
import config

settings = config.Settings()
database_path = settings.render_database_file
clients = settings.clients


def main():
    increment = 2

    test_db = Database(database_path)
    test_db.disable_all()
    test_db.save_csv()
    time.sleep(1 * increment)
    test_db.enable(4)
    test_db.save_csv()
    time.sleep(2 * increment)
    for x in range(10):
        test_db.busy(x)
        test_db.set_host(x, clients[x + 6])
        test_db.set_ifd(x, "/LOSTBOYS/FX/STUDENTS/FXTD_008/Jeronimo/blah.ifd")
        test_db.set_start_time(x, x)
        test_db.set_progress(x, x / 10.0)
    test_db.save_csv()
    time.sleep(2 * increment)
    for x in range(5):
        test_db.clean(x)
    test_db.save_csv()
    time.sleep(2 * increment)
    test_db.enable_all()
    test_db.save_csv()
    time.sleep(2 * increment)
    test_db.disable_all()
    test_db.save_csv()
    time.sleep(2 * increment)
    test_db.reset_to_defaults()
    test_db.save_csv()

if __name__ == "__main__":
    main()
    sys.exit()
