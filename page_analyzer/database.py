import os
from dotenv import load_dotenv
import psycopg2
from datetime import datetime
from psycopg2.extras import NamedTupleCursor
import requests


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
                (url, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
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


def make_check(id):
    url = find_by_id(id).name
    r = requests.get(url)
    status_code = r.status_code
    with connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute(
                """
                INSERT INTO url_checks (url_id, status_code, created_at)
                VALUES (%s, %s, %s);
                """,
                (id, status_code,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")),)


def get_checks(id):
    with connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute(("""SELECT * FROM url_checks WHERE url_id=%s"""), (id,))
            return cur.fetchall()


def get_short_info():
    with connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute("""SELECT urls.id,
                                  urls.name,
                                  MAX(url_checks.created_at) AS created_at,
                                  url_checks.status_code
                         FROM urls
                         LEFT JOIN url_checks ON
                                  urls.id = url_checks.url_id
                         GROUP BY urls.id, url_checks.status_code
                         ORDER BY urls.id DESC;""")
            return cur.fetchall()
