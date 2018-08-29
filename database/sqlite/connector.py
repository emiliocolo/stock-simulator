import sqlite3
from sqlite3 import Error

def connect_to_database(database=None, isolation_level=None, logger=None):
    """
    Connect to a sqlite database. Don't forget to close the connection at the
    end of the routine with `conn.close()`.
    Args:
        database (str): Database filename.
    Returns:
        conn (object): Connector object.
    """
    if database is None:
        database = ':memory:'
    try:
        conn = sqlite3.connect(database, isolation_level=None)
        return conn

    except Error as e:
        logger.info(e)

    return None

def disconnect_database(conn, logger):
    """
    Disconnect from sqlite database.
    """
    conn.close()
