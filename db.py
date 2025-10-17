import sqlite3

from flask import g

import config
from utilities import use_default_if_list_none
from enums import RespType, QueryType


def get_connection():
    con = sqlite3.connect(config.database_name)
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con


def execute(sql, params=None):
    params = use_default_if_list_none(params)

    # There seems to be a bug (?) in the course material as the connection doesn't close after
    # exception is thrown when unique constraint fails which causes the database connection
    # not to close which in turn locks the database before restart. If we want to continue
    # using the application after an sql exception is thrown we need to close the connection.
    lastrowid = None
    try:
        # A Connection object can be used as a context manager that automatically commits or rolls back
        # open transactions when leaving the body of the context manager.
        with get_connection() as con:
            result = con.execute(sql, params)
            lastrowid = result.lastrowid
    finally:
        # This would seem to make sense? Otherwise the last insert id might not be what we expected if
        # the previous insert caused an exception.
        g.last_insert_id = lastrowid
        # The context manager neither implicitly opens a new transaction nor closes the connection.
        con.close()


def last_insert_id():
    return g.last_insert_id


def query(sql, params=None, querytype=QueryType.ALL):
    params = use_default_if_list_none(params)

    con = get_connection()
    result = con.execute(sql, params).fetchall() if querytype == QueryType.ALL else con.execute(sql, params).fetchone()
    con.close()
    return result


def query_dict(sql, params=None):
    params = use_default_if_list_none(params)

    result = query(sql, params)

    if result:
        return [dict(row) for row in result]

    return result


def fetch_all_from_db(sql, params=None, resp_type=RespType.DEFAULT):
    return query_dict(sql, params) if resp_type == RespType.DICT else query(sql, params)


def fetch_one_from_db(sql, params=None):
    return query(sql, params, QueryType.ONE)
