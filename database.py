import sqlite3

class Database:
    # create a database for challenges.
    # each challenge has a unique id, name, an assigned member, and a start time
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS challenge (id text, name text, member text, start_time text)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS members (id text, name text)")
        self.conn.commit()
    
    def fetch_challenge(self, id):
        self.cur.execute("SELECT * FROM challenge WHERE id=?", (id,))
        rows = self.cur.fetchone()
        return rows
    
    def fetchall_challenge(self):
        self.cur.execute("SELECT * FROM challenge")
        rows = self.cur.fetchall()
        return rows

    def insert_challenge(self, id, name, member, start_time):
        self.cur.execute("INSERT INTO challenge VALUES (?, ?, ?, ?)", (id, name, member, start_time))
        self.conn.commit()

    def remove_challenge(self, id):
        self.cur.execute("DELETE FROM challenge WHERE id=?", (id,))
        self.conn.commit()
    
    def update_challenge(self, id, name, member, start_time):
        self.cur.execute("UPDATE challenge SET name = ?, member = ?, start_time = ? WHERE id = ?", (name, member, start_time, id))
        self.conn.commit()

    def fetch_member(self, id):
        self.cur.execute("SELECT * FROM members WHERE id=?", (id,))
        rows = self.cur.fetchone()
        return rows

    def fetchall_member(self):
        self.cur.execute("SELECT * FROM members")
        rows = self.cur.fetchall()
        return rows

    def insert_member(self, id, name):
        self.cur.execute("INSERT INTO members VALUES (?, ?)", (id, name))
        self.conn.commit()

    def remove_member(self, id):
        self.cur.execute("DELETE FROM members WHERE id=?", (id,))
        self.conn.commit()
    
    def update_member(self, id, name):
        self.cur.execute("UPDATE members SET name = ? WHERE id = ?", (name, id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
    
    def clear(self):
        self.cur.execute("DELETE FROM challenge")
        self.cur.execute("DELETE FROM members")
        self.conn.commit()


# db = Database('store.db')