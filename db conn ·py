"""Safu ndogo ya muunganisho wa database.

- Ukiweka `DATABASE_URL` kwenye Streamlit Secrets (mf. kiungo cha Neon Postgres),
  data yote inahifadhiwa kwenye Postgres inayodumu.
- Usipoiweka, inatumia faili la SQLite la ndani (inafaa kwa majaribio kwenye kompyuta yako,
  lakini HAIDUMU kwenye Streamlit Cloud).

SQL inaandikwa mara moja kwa kutumia `?` kama kishika-nafasi; hapa tunaibadilisha
kuwa `%s` kwa Postgres.
"""
import os
import sqlite3

try:
    import streamlit as st
except ImportError:  # k.m. majaribio nje ya Streamlit
    st = None


def database_url():
    try:
        url = st.secrets.get("DATABASE_URL", "")
    except Exception:
        url = ""
    return str(url or os.environ.get("DATABASE_URL", "")).strip()


def ni_postgres():
    return database_url().startswith(("postgres://", "postgresql://"))


def _makosa(jina):
    """Kusanya aina ya kosa kutoka sqlite3 na (kama ipo) psycopg."""
    aina = [getattr(sqlite3, jina)]
    try:
        import psycopg

        aina.append(getattr(psycopg, jina))
    except ImportError:
        pass
    return tuple(aina)


IntegrityError = _makosa("IntegrityError")
Error = _makosa("Error")


class _Cursor:
    """Cursor nyepesi inayofanya kazi sawa kwa sqlite na psycopg."""

    def __init__(self, conn):
        self._conn = conn
        self._cur = None

    def execute(self, sql, params=()):
        self._cur = self._conn.execute(sql, params)
        return self

    def fetchone(self):
        return self._cur.fetchone()

    def fetchall(self):
        return self._cur.fetchall()

    @property
    def rowcount(self):
        return self._cur.rowcount

    def __iter__(self):
        return iter(self._cur)


class Muunganisho:
    def __init__(self, raw, pg):
        self.raw = raw
        self.pg = pg

    def execute(self, sql, params=()):
        if self.pg:
            sql = sql.replace("?", "%s")
        return self.raw.execute(sql, tuple(params))

    def cursor(self):
        return _Cursor(self)

    def commit(self):
        self.raw.commit()

    def rollback(self):
        self.raw.rollback()

    def close(self):
        self.raw.close()


def connect(sqlite_path):
    """Fungua muunganisho. `sqlite_path` hutumika tu kama DATABASE_URL haijawekwa."""
    url = database_url()
    if url.startswith(("postgres://", "postgresql://")):
        import psycopg

        # prepare_threshold=None: salama na pooler ya Neon (PgBouncer).
        raw = psycopg.connect(url, connect_timeout=15, prepare_threshold=None)
        return Muunganisho(raw, True)
    raw = sqlite3.connect(sqlite_path, timeout=30.0, check_same_thread=False)
    return Muunganisho(raw, False)


def ongeza_safu_kama_haipo(conn, jedwali, safu, aina):
    """Ongeza safu mpya kwenye jedwali la zamani bila kufuta data."""
    if conn.pg:
        conn.execute(f"ALTER TABLE {jedwali} ADD COLUMN IF NOT EXISTS {safu} {aina}")
        return
    zilizopo = {r[1] for r in conn.execute(f"PRAGMA table_info({jedwali})").fetchall()}
    if safu not in zilizopo:
        conn.execute(f"ALTER TABLE {jedwali} ADD COLUMN {safu} {aina}")


def aina_ya_id(conn):
    """Safu ya namba ya kujiongeza yenyewe: SERIAL kwa Postgres, AUTOINCREMENT kwa SQLite."""
    return "SERIAL PRIMARY KEY" if conn.pg else "INTEGER PRIMARY KEY AUTOINCREMENT"
