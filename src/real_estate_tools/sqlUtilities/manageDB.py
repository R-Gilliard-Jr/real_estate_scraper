import sqlite3
import os

def getDB():
    dirname = os.path.dirname(__file__)
    db_path = os.path.join(
        dirname, "database", "property_data.db"
    )
    db = sqlite3.connect(db_path)

    db.row_factory = sqlite3.Row

    return db

def closeDB(db = None):
    if db is not None:
        db.close()

def initDB():

    dirname = os.path.dirname(__file__)

    try:
        path = os.path.join(dirname, "database")
        os.makedirs(path)
    except OSError:
        pass

    db = getDB()
    schema = os.path.join(os.path.dirname(__file__), "schema.sql")
    with open(schema) as f:
        db.executescript(f.read())