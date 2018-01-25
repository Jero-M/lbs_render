#!/usr/bin/python
import os
import signal
import subprocess
import shlex

import gtk
import appindicator


class AppIndicator:
    def __init__(self):
        self.ind = appindicator.Indicator(
                                    "lbs-render",
                                    "indicator-messages",
                                    appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.ind.set_attention_icon("indicator-messages-new")
        self.ind.set_icon(project_path + "/img/app_logo.png")

        self.menu = gtk.Menu()
        open_control_panel = gtk.MenuItem("Control Panel")
        open_control_panel.connect("activate", open_ui)
        open_control_panel.show()
        self.menu.append(open_control_panel)

        enable_render = gtk.MenuItem("Enable Rendering")
        enable_render.connect("activate", enable)
        enable_render.show()
        self.menu.append(enable_render)

        disable_render = gtk.MenuItem("Disable Rendering")
        disable_render.connect("activate", disable)
        disable_render.show()
        self.menu.append(disable_render)

        quit_item = gtk.MenuItem("Quit")
        quit_item.connect("activate", self.quit)
        quit_item.show()
        self.menu.append(quit_item)

        self.menu.show()

        self.ind.set_menu(self.menu)

    def quit(self, widget, data=None):
        for pid in child_pids:
            try:
                os.kill(pid, signal.SIGKILL)
            except:
                continue
        gtk.main_quit()


def disable(*kwargs):
    disable_file = project_path + "/disable_host.py"
    cmd = disable_file
    process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
    if process.pid not in child_pids:
        child_pids.append(process.pid)


def enable(*kwargs):
    enable_file = project_path + "/enable_host.py"
    cmd = enable_file
    process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
    if process.pid not in child_pids:
        child_pids.append(process.pid)


def open_ui(*kwargs):
    control_panel_file = project_path + "/control_panel.py"
    cmd = control_panel_file
    process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
    if process.pid not in child_pids:
        child_pids.append(process.pid)


def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    project_path = os.path.dirname(os.path.realpath(__file__))
    child_pids = []
    # App Indicator
    indicator = AppIndicator()
    main()
