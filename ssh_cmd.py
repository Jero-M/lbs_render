#!/usr/bin/python
from pexpect import pxssh
import sys

def ssh_start(client, username):
    ssh_connection = pxssh.pxssh(timeout=None)
    ssh_connection.logfile = sys.stdout
    ssh_connection.login(client, username)
    return ssh_connection

def send_cmd(ssh_obj, command):
    ssh_obj.sendline(command)
