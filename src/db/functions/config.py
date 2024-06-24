import psycopg2

DB_HOST = "localhost"
DB_NAME = "shorter_url"
DB_USER = "postgres"
DB_PASSWORD = "123"


class Database:
    def __init__(self):
        self.host = DB_HOST
        self.database = DB_NAME
        self.user = DB_USER
        self.password = DB_PASSWORD
        self.conn = None

    def connect(self):
        self.conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password,
        )
        self.cur = self.conn.cursor()

    def disconnect(self):
        self.cur.close()
        self.conn.close()
    
    def test(self):
        print('teste')