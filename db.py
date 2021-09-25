import sqlite3


class SQLighter:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def init_db(self):
        with self.connection:
            self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS person (
                        cid             INTEGER PRIMARY KEY,
                        name            TEXT,
                        alias           TEXT,
                        first_name      TEXT NOT NULL,
                        last_name       TEXT NOT NULL,
                        is_registered   BOOLEAN,
                        has_cv          BOOLEAN,
                        completed_test  BOOLEAN,
                        phone           TEXT NOT NULL,
                        email           TEXT NOT NULL,
                        cv_link         TEXT,
                        balance         INTEGER,
                        test_num        INTEGER,
                        test_score      INTEGER
                    )
                ''')

    def find_all(self):
        """ Найти всех пользователей """
        with self.connection:
            return self.cursor.execute('SELECT * FROM person').fetchall()

    def find_user(self, cid: int):
        with self.connection:
            return self.cursor.execute('SELECT * FROM person WHERE cid = ?', cid).fetchall()

    def add_user(self, cid: int, name: str, first_name: str,
                 last_name: str, alias: str,
                 phone: str, email: str):
        with self.connection:
            self.cursor.execute('''
                INSERT INTO person (cid, name, alias, first_name, last_name, is_registered, has_cv, completed_test, phone, email, balance, test_num, test_score) 
                VALUES (?, ?, ?, ?, ?, true, false, false, ?, ?, 0, 0, 0
                )
                ''', (cid, name, alias, first_name, last_name, phone, email))

    def update_user_balance(self, cid: int, balance: int):
        with self.connection:
            self.cursor.execute('''
                UPDATE person SET balance = ?
                WHERE cid = ? 
            ''', (balance, cid))

    def update_user_cv(self, cid: int,
                       cv_link: str):
        with self.connection:
            self.cursor.execute('''
                UPDATE person SET cv_link = ?
                WHERE cid = ? 
            ''', (cv_link, cid))

    def update_user_test_num(self, cid: int,
                             test_num: int):
        with self.connection:
            self.cursor.execute('''
                   UPDATE person SET test_num = ?
                   WHERE cid = ? 
               ''', (test_num, cid))

    def update_user_test_score(self, cid: int,
                               test_score: int):
        with self.connection:
            self.cursor.execute('''
                   UPDATE person SET test_score = ?
                   WHERE cid = ? 
               ''', (test_score, cid))

    def update_user_cv_add(self, cid: int):
        with self.connection:
            self.cursor.execute('''
                UPDATE person SET has_cv = ? 
                WHERE cid = ? 
            ''', (True, cid))

    def update_user_finish_test(self, cid: int):
        with self.connection:
            self.cursor.execute('''
                UPDATE person SET completed_test = ?
                WHERE cid = ? 
            ''', (True, cid))

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()
