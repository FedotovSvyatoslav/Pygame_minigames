import sqlite3

CREATE_TABLE_SQL_FILE = "sql_scripts/create_table.sql"
ADD_EMPTY_ROW_SQL_FILE = "sql_scripts/add_empty_row.sql"
SET_SCORE = "sql_scripts/set_score.sql"
GET_SCORE = "sql_scripts/get_score.sql"


def create_table_and_add_row(db_name):
    db_connection = sqlite3.connect(db_name)
    db_cursor = db_connection.cursor()
    with open(CREATE_TABLE_SQL_FILE, 'rt') as sql_file:
        db_cursor.execute(sql_file.read())
    with open(ADD_EMPTY_ROW_SQL_FILE, 'rt') as sql_file:
        db_cursor.execute(sql_file.read())
    db_connection.commit()


def set_score(db_name, score):
    db_connection = sqlite3.connect(db_name)
    db_cursor = db_connection.cursor()
    with open(SET_SCORE, 'rt') as sql_file:
        db_cursor.execute(sql_file.read(), (score, )).fetchall()
    db_connection.commit()


def get_score(db_name):
    db_connection = sqlite3.connect(db_name)
    db_cursor = db_connection.cursor()
    with open(GET_SCORE, 'rt') as sql_file:
        result = db_cursor.execute(sql_file.read()).fetchall()
    return result
