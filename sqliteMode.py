#import modules
import os
import sqlite3 as sq

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

db_path = 'bd.db'


# Check if database exists, create if it doesn't
if not os.path.exists(db_path):
    open(db_path, 'w').close()


# Connecting to a database and creating a cursor
con = sq.connect(db_path, check_same_thread=False)
cur = con.cursor()


def TableExists(table_name):
    """Check if a table exists in the database"""
    cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    if cur.fetchone()[0] == 1:
        return True
    else:
        return False


def CreateTable(table_name):
    """Create a table in the database"""
    ("start CreateTable")
    columns = ""
    match table_name:
        case 'users':
            columns = 'id TEXT PRIMARY KEY, name TEXT, numb TEXT, id_tg TEXT, surname TEXT'
        case 'trips':
            # columns = 'user_id TEXT, typeofmembers TEXT, tripsdates TEXT, tripstimes TEXT, direction_name TEXT, route_number TEXT, pointa TEXT, pointb TEXT, id_trip TEXT, number_of_passengers TEXT, status TEXT'
            # new version of table VVVVVVVV
            columns = 'user_id TEXT, typeofmembers TEXT, tripsdates TEXT, tripstimes TEXT, direction_name TEXT, route_number INTEGER, pointa INTEGER, pointb INTEGER, id_trip TEXT, number_of_passengers INTEGER, status TEXT'
        case 'transactions':
            columns = 'id TEXT PRIMARY KEY, user_id, summ TEXT, date_time TEXT, type_of_transaction TEXT'
        case 'drivers':
            columns = 'user_id TEXT, brand TEXT, colour TEXT, numbcar TEXT, car_id TEXT'
        case 'balance':
            columns = 'id TEXT PRIMARY KEY, user_id TEXT, summ TEXT'
        case 'agreedTrips':
            # columns = 'id_trip TEXT, tripsdates TEXT, tripstimes TEXT, pointa TEXT, pointb TEXT, number_of_passengers TEXT, id_driver TEXT, id_passenger TEXT, status TEXT, ids_trips TEXT, maximum_number_of_passengers TEXT'
            # new version of table VVVVVVVV
            columns = 'agreeding_trips_id TEXT, driver_trip_id TEXT, maximum_number_of_passengers INTEGER, number_of_passengers INTEGER, ids_trips TEXT, status TEXT'
        case 'agreement':
            columns = 'id_agreement TEXT, id_user TEXT, response INT, datetime TEXT'
        case _:
            raise ValueError(f"Unknown table name '{table_name}'")
    cur.execute(f"CREATE TABLE {table_name}({columns})")


def CheckUserIdTg(id_tg):
    """Checking users by telegram id"""
    cur.execute("SELECT name, id FROM USERS WHERE id_tg = ?", (id_tg,))
    try:
        return [dict(zip([key[0] for key in cur.description], row)) for row in cur.fetchall()][0]
    except Exception as e:
        return []


def InsertData(T, V, C=""):
    """Entering data into the database"""
    try:
        if not TableExists(T):
            CreateTable(T)
        cur.execute(f'INSERT INTO {T} {C} VALUES({V})')
        con.commit()
        return [1, 2]
    except Exception as e:
        return []


def DeleteData(T, V, C):
    """Delete data into the database"""
    try:
        cur.execute(f'DELETE FROM {T} WHERE {V} = ?', (C,))
        con.commit()
        return[1, 2]
    except Exception as e:
        return []



def SelectData(T, C, V, S="*"):
    """Sending data from the database"""
    try:
        cur.execute(f'SELECT {S} FROM {T} WHERE {C} = "{V}"')
        return [dict(zip([key[0] for key in cur.description], row)) for row in cur.fetchall()][0]
    except Exception as e:
        return []



def UpdateData(T, U, S, C, V):
    """Edit data from the database"""
    try:
        cur.execute(f'UPDATE {T} SET {U} = ({S}) WHERE {C} = "{V}"')
        con.commit()
        return[1, 2]
    except Exception as e:
        return[e]



def SelectAllData(T, C, V, S="*"):
    """Sending an array of data from a database"""
    try:
        cur.execute(f'SELECT {S} FROM {T} WHERE {C} = "{V}"')
        data = cur.fetchall()
        newList = [
            [
                dict(zip([key[0] for key in cur.description], row))
                for row in data
            ][i]
            for i in range(len(data))
        ]
        return newList
    except Exception as e:
        return []
