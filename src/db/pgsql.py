import psycopg2

DB_HOST = "localhost"
DB_NAME = "shorter-url"
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

    def create_table(self):
        self.cur.execute(
            """
            CREATE TABLE if not exists url (
                id SERIAL PRIMARY KEY,
                original_url VARCHAR(255) NOT NULL,
                shorter_url VARCHAR(255) NOT NULL
            )
            """
        )
        self.conn.commit()

    def get_urls(self):
        self.cur.execute("SELECT * FROM url;")
        rows = self.cur.fetchall()
        urls = []
        for row in rows:
            url = {"id": row[0], "original_id": row[1], "shorter_id": row[2]}
            urls.append(url)

        return urls

    def get_url(self, id):
        self.cur.execute(f"SELECT * FROM url WHERE id = {id};")
        return self.cur.fetchone()

    def create_url(self, original_url, shorter_url):
        self.cur.execute(
            """
            INSERT INTO url (original_url, shorter_url)
                VALUES (%s, %s)
                RETURNING *;
            """,
            (original_url, shorter_url),
        )
        self.conn.commit()
        new_url = self.cur.fetchone()
        new_url = {
            "id": new_url[0],
            "original_id": new_url[1],
            "shorter_id": new_url[2],
        }
        return new_url

    def delete_url(self, id):
        self.cur.execute(f"DELETE FROM url WHERE id = {id};")
        self.conn.commit()
