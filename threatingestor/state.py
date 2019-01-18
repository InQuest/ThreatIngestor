import sqlite3

class State():
    def __init__(self, dbname):
        
        self.conn  =  sqlite3.connect(dbname)
        self._create_table()

    def _create_table(self):
        c = self.conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS states (name text UNIQUE, state text)''')

        self.conn.commit()
        

    def save_state(self, name, state):
        c = self.conn.cursor()
        c.execute('''INSERT OR REPLACE INTO states (name, state) values (?,?)''',(name,state))

        self.conn.commit()

    def get_state(self, name):
        c = self.conn.cursor()
        c.execute('''SELECT state FROM states WHERE name=?''',(name,)) 
        res= c.fetchone()
        return res[0] if res else res

    def close(self):
        self.conn.close()
