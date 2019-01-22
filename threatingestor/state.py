import sqlite3

class State:

    def __init__(self, dbname):
        self.conn = sqlite3.connect(dbname)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS states (name text UNIQUE, state text)')
        self.conn.commit()

    def save_state(self, name, state):
        self.cursor.execute('INSERT OR REPLACE INTO states (name, state) values (?, ?)', (name, state))
        self.conn.commit()

    def get_state(self, name):
        self.cursor.execute('SELECT state FROM states WHERE name=?', (name,))
        res = self.cursor.fetchone()
        return res[0] if res else res
