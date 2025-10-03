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

    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid
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
