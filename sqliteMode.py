#import modules 
import sqlite3 as sq



#Connecting to a database and creating a cursor
con = sq.connect("bd.db", check_same_thread=False)
cur = con.cursor()




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
        cur.execute(f'INSERT INTO {T} {C} VALUES({V})')
        con.commit()
        return[1, 2]
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


