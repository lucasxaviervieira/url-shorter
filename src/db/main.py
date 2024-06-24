import psycopg2
import base64

from db.functions import gen_qrcode as qc

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

    def start(self):
        self.connect()
        self.create_table()

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
                shorter_url VARCHAR(255) NOT NULL,
                svg_data BYTEA
            )
            """
        )
        self.conn.commit()

    def get_urls(self):
        self.cur.execute("SELECT * FROM url;")
        urls = self.cur.fetchall()
        url_list = []
        for url in urls:
            new_url = self.api_response(url)
            url_list.append(new_url)
        return url_list

    def get_url(self, attribute, value):
        self.cur.execute(f"SELECT * FROM url WHERE {attribute} = '{value}';")
        url = self.cur.fetchone()
        new_url = self.api_response(url)
        return new_url

    def create_url(self, original_url):     
        next_id = self.get_next_id()       
        local_url = "http://127.0.0.1:5000/"
        shorter_url = local_url + str(next_id)
        
        svg_string = qc.generate_qr_code(shorter_url)

        self.cur.execute(
            """
            INSERT INTO url (original_url, shorter_url, svg_data)
                VALUES (%s, %s, E%s)    
                RETURNING *;
            """,
            (original_url, shorter_url, svg_string),
        )
        self.conn.commit()
        url = self.cur.fetchone()
        new_url = self.api_response(url)
        return new_url

    def delete_url(self, id):
        self.cur.execute(f"DELETE FROM url WHERE id = {id};")
        self.conn.commit()

    def url_exists(self, attribute, value):
        self.cur.execute(
            f"SELECT EXISTS (SELECT 1 FROM url WHERE {attribute} = '{value}');"
        )
        url_exists = self.cur.fetchone()
        return url_exists[0]

    def api_response(self, url):
        bytea = self.read_svg_bytea(url[3])
        new_url = {
            "id": url[0],
            "original_url": url[1],
            "shorter_url": url[2],
            "svg_qrcode": bytea,
        }
        return new_url

    def read_svg_bytea(self, bytea_value):
        encoded_data = base64.b64encode(bytea_value).decode("utf-8")
        decoded_data = base64.b64decode(encoded_data.encode("utf-8"))
        decoded_data = decoded_data.decode("utf-8")
        svg_string = decoded_data.replace('"', "'")
        svg_string = svg_string.replace("\n", "")
        return svg_string
    
    def get_next_id(self):
        self.cur.execute("SELECT * from url_id_seq")
        id = self.cur.fetchone()
        next_id = id[0] + 1 
        return next_id
