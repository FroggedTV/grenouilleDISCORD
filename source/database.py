from threading import Lock
import sqlite3
import config
import logging
from time import time as current_time

LOGGER = logging.getLogger(__name__)


class Database(object):
    def __init__(self):
        LOGGER.debug("Initializing Database object")
        self.database_path = config.database_path
        self.lock = Lock()
        self.connection = sqlite3.connect(self.database_path,
            check_same_thread=False)
        self.init_table()

    def init_table(self):
        self.lock.acquire()
        c = self.connection.cursor()
        query = '''CREATE TABLE IF NOT EXISTS alerts
                (
                    game_id INTEGER,
                    status TEXT,
                    time INTEGER
                );'''
        c.execute(query)
        self.connection.commit()
        self.lock.release()

    def insert_alert(self, game_id, status):
        LOGGER.debug("Inserting alert: "+str(game_id)+" "+status)
        self.lock.acquire()
        c = self.connection.cursor()
        alert_time = int(current_time())
        c.execute('INSERT INTO alerts VALUES (?, ?, ?)', (game_id, status, alert_time))
        self.connection.commit()
        self.lock.release()

    def is_alert(self, game_id, status):
        self.lock.acquire()
        c = self.connection.cursor()
        c.execute('SELECT game_id FROM alerts WHERE game_id = ? AND status = ?', (game_id, status))
        content = c.fetchone()
        self.lock.release()
        if content:
            return True
        else:
            return False
