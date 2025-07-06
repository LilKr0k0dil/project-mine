import sqlite3

class Database:
    
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        
    def add_account(self, id, nickname):
        self.cursor.execute("INSERT INTO accounts (tg_id, nickname) VALUES (?,?)",(id, nickname))
        self.conn.commit()
        
    def check_account(self,id):
        return self.cursor.execute("SELECT * FROM accounts WHERE `tg_id` = ?",(id,)).fetchone() == None

    
    def change_nickname(self, id, nickname):
        self.cursor.execute("UPDATE accounts SET nickname = ? WHERE tg_id = ?",(nickname, id))
        self.conn.commit()
        
    def get_nickname(self, id):
        return self.cursor.execute("SELECT nickname FROM accounts WHERE tg_id = ?",(id,)).fetchone()[0]
    
    def find_by_nickname(self,nickname):
        return self.cursor.execute("SELECT tg_id FROM accounts WHERE nickname = ?",(nickname,)).fetchone()[0]
    
    def is_banned(self, id) -> bool:
        return self.cursor.execute("SELECT banned FROM accounts WHERE tg_id = ?",(id,)).fetchone()[0] == 1
    
    def ban(self, nickname):
        self.cursor.execute("UPDATE accounts SET banned = 1 WHERE tg_id =?",(self.find_by_nickname(nickname),))
        self.conn.commit()