#!/usr/bin/python
import sqlite3
import sys

import config

def create_database(db_name, data):
    try:
        delete_table(db_name)
    except:
        pass
    create_table(db_name)
    insert_clients(db_name, data)

def create_table(db_name):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE Clients
                         (id INTEGER PRIMARY KEY,
                          client TEXT,
                          status TEXT,
                          host TEXT,
                          ifd TEXT,
                          start_time TEXT,
                          progress TEXT,
                          pids TEXT)""")
        db.commit()

def delete_table(db_name):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("""DROP TABLE Clients""")
        db.commit()

def insert_clients(db_name, values):
    sql = """INSERT INTO Clients
                                (client,
                                status,
                                host,
                                ifd,
                                start_time,
                                progress,
                                pids)
                                VALUES (?, ?, ?, ?, ?, ?, ?)"""
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.executemany(sql, values)
        db.commit()

def reset_to_defaults(db_name):
    '''Reset every row to [id, client, "Availble", 0, 0, 0 ,0, 0]'''
    sql = """UPDATE Clients SET status=?,
                                host=?,
                                ifd=?,
                                start_time=?,
                                progress=?,
                                pids=?"""
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute(sql, ("Available", "None", "None", "None", "None",
                             "None"))
        db.commit()

def disable_all(db_name):
    '''Disable all clients'''
    sql = """UPDATE Clients SET status=?"""
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute(sql, ("Disabled",))
        db.commit()

def enable_all(db_name):
    '''Enable all clients'''
    sql = """UPDATE Clients SET status=?"""
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute(sql, ("Available",))
        db.commit()

def get_all_clients(db_name):
    '''Return a list of all the clients'''
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT client FROM Clients""")
        clients = [str(x[0]) for x in cursor.fetchall() ]
        return clients

def get_available_clients(db_name):
    '''Return a list of all the available clients'''
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT client, status FROM Clients
                          WHERE status=?""", ("Available",))
        available_clients = [str(x[0]) for x in cursor.fetchall() ]
        return available_clients

def get_row(db_name, id):
    '''Return a single row'''
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT * FROM CLIENTS WHERE id=?""", (id,))
        row = [str(x) for x in cursor.fetchone()]
        return row

def get_id(db_name, host):
    '''Return the ID based on host'''
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT * FROM CLIENTS WHERE client=?""", (host,))
        id = cursor.fetchone()[0]
        return id

def get_client(db_name, id):
    '''Return the client name of a row based on id'''
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT client FROM CLIENTS WHERE id=?""", (id,))
        return str(cursor.fetchone()[0])

def get_status(db_name, id):
    '''Return the status of a row based on id'''
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT status FROM CLIENTS WHERE id=?""", (id,))
        return str(cursor.fetchone()[0])

def get_host(db_name, id):
    '''Return the host name of a row based on id'''
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT host FROM CLIENTS WHERE id=?""", (id,))
        return str(cursor.fetchone()[0])

def get_ifd(db_name, id):
    '''Return the ifd path of a row based on id'''
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT ifd FROM CLIENTS WHERE id=?""", (id,))
        return str(cursor.fetchone()[0])

def get_start_time(db_name, id):
    '''Return the start time of a row based on id'''
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT start_time FROM CLIENTS WHERE id=?""", (id,))
        return str(cursor.fetchone()[0])

def get_progress(db_name, id):
    '''Return the progress of a row based on id'''
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT progress FROM CLIENTS WHERE id=?""", (id,))
        return str(cursor.fetchone()[0])

def get_pids(db_name, id):
    '''Return the pids related to the render of a row based on id'''
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT pids FROM CLIENTS WHERE id=?""", (id,))
        pids = str(cursor.fetchone()[0])
    if pids == "None":
        return None
    else:
        return map(int, pids.split("-"))

def disable(db_name, id):
    '''Set status of a single client to Disabled'''
    sql = """UPDATE Clients SET status=? WHERE id=?"""
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute(sql, ("Disabled", id))
        db.commit()

def enable(db_name, id):
    '''Set status of a single client to Disabled'''
    sql = """UPDATE Clients SET status=? WHERE id=?"""
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute(sql, ("Available", id))
        db.commit()

def busy(db_name, id):
    '''Set status of a single client to Rendering'''
    sql = """UPDATE Clients SET status=? WHERE id=?"""
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute(sql, ("Rendering", id))
        db.commit()

def set_host(db_name, id, host_name):
    '''Set host name of a single client'''
    assert type(host_name) == type("str")
    sql = """UPDATE Clients SET host=? WHERE id=?"""
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute(sql, (host_name, id))
        db.commit()

def set_ifd(db_name, id, ifd_path):
    '''Set the ifd path of single client'''
    assert type(ifd_path) == type("str")
    sql = """UPDATE Clients SET ifd=? WHERE id=?"""
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute(sql, (ifd_path, id))
        db.commit()

def set_start_time(db_name, id, new_time):
    '''Set the start time of single client'''
    sql = """UPDATE Clients SET start_time=? WHERE id=?"""
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute(sql, (new_time, id))
        db.commit()

def set_progress(db_name, id, new_progress):
    '''Set the progress of single client'''
    sql = """UPDATE Clients SET progress=? WHERE id=?"""
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute(sql, (new_progress, id))
        db.commit()

def add_pid(db_name, id, pid):
    '''Add the PID of a process being used by a single client'''
    sql = """UPDATE Clients SET pids=? WHERE id=?"""
    try:
        pid = int(pid)
    except:
        return
    pids = get_pids(db_name, id)
    if pids == None:
        with sqlite3.connect(db_name) as db:
            cursor = db.cursor()
            cursor.execute(sql, (str(pid), id))
            db.commit()
    else:
        if pid not in pids:
            pids.append(pid)
            with sqlite3.connect(db_name) as db:
                cursor = db.cursor()
                cursor.execute(sql, ("-".join(map(str, pids)), id))
                db.commit()

def remove_pid(db_name, id, pid):
    '''Remove the PID of a process being used by a single client''' 
    sql = """UPDATE Clients SET pids=? WHERE id=?"""
    try:
        pid = int(pid)
    except:
        return
    pids = get_pids(db_name, id)
    if pids == None:
        return
    else:
        if pid not in pids:
            return
        else:
            pids.remove(pid)
            if len(pids) == 0:
                pid = "None"
            else:
                pid = "-".join(map(str, pids))
            with sqlite3.connect(db_name) as db:
                cursor = db.cursor()
                cursor.execute(sql, (pid, id))
                db.commit()

def clean(db_name, id):
    '''Reset a single row'''
    sql = """UPDATE Clients SET status=?,
                                host=?,
                                ifd=?,
                                start_time=?,
                                progress=?,
                                pids=?
                                WHERE id=?"""
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute(sql, ("Available", "None", "None", "None", "None",
                             "None", id))
        db.commit()


if __name__ == "__main__":
    settings = config.Settings()
    database_path = settings.render_database_file
    database_rows = []
    for client in settings.clients:
        database_rows.append((client, "Available", "None",
                              "None", "None", "None", "None"))
    
    # create_database(database_path, database_rows)
    # get_available_clients(database_path)
    # disable_all(database_path)
    # enable(database_path, 3)
    # print get_pids(database_path, 10)
    # busy(database_path, 3)
    # set_progress(database_path, 1, "None")
    # remove_pid(database_path, 2, 2345)
    # clean(database_path, 4)
    # print get_all_clients(database_path)
    reset_to_defaults(database_path)

    sys.exit()