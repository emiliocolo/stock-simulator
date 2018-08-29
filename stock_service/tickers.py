"""
SEOUL AI TICKER Fake Simulator
Emilio Coronado, emilio.mobile@gmail.com
seoulai.com
2018
"""

import threading
import time as t
import datetime
import random
from database.sqlite.connector import *
from database.sqlite.create_table import *
from flask_socketio import SocketIO, emit

class Ticker(threading.Thread):
    BASE_PRICE = 100
    LAST_PRICE = 100
    time = ''
    selling = 0
    buying = 0
    total = 0
    increment = 0
    action = ''

    def __init__(self, name="", logger=None, server=None):

        # Set the general logger
        if logger is not None:
            self.log = logger
            self.log.info('--- Starting {} Ticker Simulation ---'.format(name))

        # Create the sqllite DB, and stock tables

        self.database = "./data/seoul_ai_gym_stocks.db"

        sql_create_stock_tickers_table = """ CREATE TABLE IF NOT EXISTS stock_tickers (
                                            date_time text NOT NULL,
                                            ticker_name text NOT NULL,
                                            ticker_value real NOT NULL
                                        ); """
        isolation_level = None # sqlite autocommit
        db_connection = connect_to_database(self.database, isolation_level, logger)

        if db_connection is not None:
            # create stock tickers table
            create_table(db_connection, sql_create_stock_tickers_table)
        else:
            logger.info("Error! cannot create the database connection.")

        # Prepare a Websocket to stream the data
        if server is not None:
            self.socketio = SocketIO(server)
            @self.socketio.on('connect')
            def test_connect():
                print('SERVER: Websocket: Client connected')

            @self.socketio.on('disconnect')
            def test_disconnect():
                print('SERVER: Websocket: Client disconnected')

            @self.socketio.on('my_event')
            def handle_message(message):
                received_message = message['data']
                print("ticker received the message: {}".format(received_message))

            self.stream = True
        else:
            self.stream = False

        threading.Thread.__init__(self)

    def select_all_tickers(self, conn):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        cur = conn.cursor()
        cur.execute("SELECT * FROM stock_tickers")

        rows = cur.fetchall()

        for row in rows:
            print(row)

    def store_ticker(self, time, name, price):
        """
        Create a new ticker in storage
        :param time:
        :param ticker_name:
        :param ticker_price:
        :return:
        """
        # Connecting to DB
        isolation_level = None # sqlite autocommit
        db_connection = connect_to_database(self.database, isolation_level, self.log)

        if db_connection is not None:
            ticker = (time, name, price)
            sql = ''' INSERT INTO stock_tickers (date_time, ticker_name, ticker_value) VALUES(?,?,?) '''
            cur = db_connection.cursor()
            cur.execute(sql, ticker)
            # Now we can disconnect from DB
            disconnect_database(db_connection, self.log)
            # self.select_all_tickers(db_connection)
            return cur.lastrowid
        else:
            self.log.info("Error! cannot create the database connection.")

        return None

    def generate(self, x):
        # Updating the new BASE_PRICE base on some basic randomness
        # In future might be brownian motion algorithm to generate the stock price.
        self.BASE_PRICE = self.LAST_PRICE

        # Generating Timestamp
        ts = t.time()
       # st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
       # st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        self.time = ts
        self.ticker = 'SEOULAI'

        # Calculate Price Up/Down/Equal
        actions = ['UP', 'DOWN']
        self.action = random.choice(actions)

        # Calculate Ticker Value
        increment_factor = random.randint(0, 5) # Set to Increments/Decrements between 0~50%
        self.increment = (self.BASE_PRICE * increment_factor) / 100

        if (self.increment == 0):
            self.action = 'EQUAL' # Nothing to be increase, but will indicate that nothing will change

        if (self.action == 'DOWN'):
            self.increment = self.increment * -1
            increment_factor = increment_factor * -1

        self.LAST_PRICE = self.BASE_PRICE + self.increment

        # Volume Parameters TODO give some randomness
        self.selling = 1000.00
        self.buying = 2000.00
        self.available = 300000

        self.log.info('%s : %s : %s : %s : %s : [%s] : %s', self.time, self.ticker, '{0:.2f}'.format(self.BASE_PRICE), '{0:.2f}'.format(self.LAST_PRICE), '{0:.2f}'.format(self.increment), increment_factor, self.action)

        # store
        self.store_ticker(self.time, self.ticker, self.LAST_PRICE)

        # stream
        if self.stream is True:
            self.socketio.emit('message', {'date': self.time, 'ticker': self.ticker, 'close': self.LAST_PRICE}, broadcast=False)

    def consume(self, ticker=""):
        # TODO: at the moment there is only one ticker supported
        return self.action, self.time, self.ticker, '{0:.2f}'.format(self.BASE_PRICE), '{0:.2f}'.format(self.LAST_PRICE), '{0:.2f}'.format(self.increment), self.selling, self.buying , self.available

    def run(self):
        for x in range(10000):
            self.generate(x)
            t.sleep(1)      # second resolution

if __name__ == '__main__':
    print("SEOULAI Ticker Simulator")
    ticker_simulator = Ticker("SEOULAI")
    ticker_simulator.start()