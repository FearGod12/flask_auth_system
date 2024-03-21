#/usr/bin/env python

from models.database.engine import Database

storage = Database()
storage.reload()