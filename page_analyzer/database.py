import os
from dotenv import load_dotenv
import psycopg2
from datetime import date
from psycopg2.extras import NamedTupleCursor


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


def connection():
    return psycopg2.connect(DATABASE_URL)


def add_to_db(url):
    with connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute(
                """
                INSERT INTO urls (name, created_at)
                VALUES (%s, %s) RETURNING id;
                """,
                (url, date.today()),
            )
            id = cur.fetchone().id
            return id


def find_by_id(id):
    with connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute("""SELECT * FROM urls WHERE id = %s;""", (id,))
            return cur.fetchone()


def find_by_url(url):
    with connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute("""SELECT * FROM urls WHERE name = %s;""", (url,))
            return cur.fetchone()


def get_all_from_db():
    with connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute("""SELECT * FROM urls ORDER BY id DESC;""")
            return cur.fetchall()
