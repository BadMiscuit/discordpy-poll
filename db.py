import sqlite3

class DbConnection:
    def __init__(self):
        pass

    def __enter__(self):
        self.conn = sqlite3.connect('bot.db')
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        try:
            self.conn.commit()
        except:
            self.conn.rollback()
        self.conn.close()

