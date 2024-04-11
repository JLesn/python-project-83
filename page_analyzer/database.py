import os
from dotenv import load_dotenv
import psycopg2
from datetime import datetime
from psycopg2.extras import NamedTupleCursor


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


def connection():
    return psycopg2.connect(DATABASE_URL)


def add_to_db(url):
    with connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute(
                "INSERT INTO urls (name, created_at) VALUES (%s, %s)",
                (url, datetime.now().strptime("%Y-%m-%d")),
            )
            return cur.fetchone()


def find_by_id(id):
    with connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE id = %s;", (id,))
            return cur.fetchone()


def find_by_url(url):
    with connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE url = %s;", (url,))
            return cur.fetchone()
