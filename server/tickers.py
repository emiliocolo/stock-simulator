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
import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


class Ticker(threading.Thread):
    BASE_PRICE = 100
    LAST_PRICE = 100
    time = ''
    selling = 0
    buying = 0
    total = 0
    increment = 0
    action = ''

    def __init__(self, name=""):
        threading.Thread.__init__(self)
        print('--- Starting {} Ticker Simulation ---'.format(name))

    def generate(self, x):

        # Updating the new BASE_PRICE
        self.BASE_PRICE = self.LAST_PRICE

        # Generating Timestamp
        ts = t.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        self.time = st
        self.ticker = 'SEOULAI'

        # Calculate Price Up/Down/Equal
        actions = ['UP', 'DOWN']
        self.action = random.choice(actions)

        # Calculate Ticker Value
        increment_factor = random.randint(0, 50) # Set to Increments/Decrements between 0~50%
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

        #logging.debug('%s : %s : %s : %s : %s : [%s] : %s', self.time, self.ticker, '{0:.2f}'.format(self.BASE_PRICE), '{0:.2f}'.format(self.LAST_PRICE), '{0:.2f}'.format(self.increment), increment_factor, self.action)


    def consume(self, ticker=""):
        # TODO: at the moment there is only one ticker supported
        return self.action, self.time, self.ticker, '{0:.2f}'.format(self.BASE_PRICE), '{0:.2f}'.format(self.LAST_PRICE), '{0:.2f}'.format(self.increment), self.selling, self.buying , self.available

    def run(self):
        for x in range(1000):
            self.generate(x)
            t.sleep(1)      # second resolution

if __name__ == '__main__':
    print("SEOULAI Ticker Simulator")
    ticker_simulator = Ticker("SEOULAI")
    ticker_simulator.start()