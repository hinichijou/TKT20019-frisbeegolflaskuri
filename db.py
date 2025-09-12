import sqlite3
from flask import g
from enum import Enum

class RespType(Enum):
    DEFAULT = 1,
    DICT = 2

def get_connection():
    con = sqlite3.connect("database.db")
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con

def execute(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid
    con.close()

def last_insert_id():
    return g.last_insert_id

def query(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    con.close()
    return result

def query_dict(sql, params=[]):
    result = query(sql, params)

    if result:
        return [dict(row) for row in result]

    return result

def query_db(sql, params=[], resp_type = RespType.DEFAULT):
    return query_dict(sql, params) if resp_type == RespType.DICT else query(sql, params)