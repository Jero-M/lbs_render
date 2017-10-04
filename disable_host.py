#!/usr/bin/python
from platform import node
import sys


import render_manager
import config


hostname = node()
settings = config.Settings()
render_db = render_manager.Database(settings.render_database_file)
render_db_id = int(render_db.get_id(hostname))
render_db.disable(render_db_id)
render_db.save_csv()
sys.exit()