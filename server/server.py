"""
REST API Server
Emilio Coronado, emilio.mobile@gmail.com
seoulai.com
2018
"""
from flask import (Flask, request, abort, jsonify, make_response, render_template)
import os
import random

# Constants
BAD_REQUEST = 400
STATUS_OK = 200
NOT_FOUND = 404
SERVER_ERROR = 500
PORT = 5000
BASE_PRICE = 100

def create_server(tickers, test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        #DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.errorhandler(BAD_REQUEST)
    def bad_request(error):
        return make_response(jsonify({'error': 'Bad request'}), BAD_REQUEST)


    @app.errorhandler(NOT_FOUND)
    def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), NOT_FOUND)


    @app.errorhandler(SERVER_ERROR)
    def server_error(error):
        return make_response(jsonify({'error': 'Server error'}), SERVER_ERROR)

    @app.route('/')
    def main():
        return render_template('main.html')

    @app.route('/ticker', methods=['POST'])
    def ticker():
        """Main API end point. Gives fake ticker information
        $ curl -X POST -H "Content-type: application/json" http://127.0.0.1:5000/ticker -d '{"ticker": "SEOULAI"}'
        Returns:
            resp (json): ticker information
        """

        action, time, ticker, base_value, new_value, increment, selling, buying , available = tickers.consume('SEOULAI')

        version = '1.0'
        return make_response(jsonify({  'version': version,
                                        'time': time,
                                        'ticker': ticker,
                                        'action': action,
                                        'value_base': base_value,
                                        'value_new': new_value,
                                #        'selling_volume': selling,
                                #        'buying_volume': buying,
                                #        'total_stocks': available,
                                #        'base_price': base,
                                #        'increment_percentage_factor': increment_factor,
                                        'value_new_increment': increment,
                                        }), STATUS_OK)
    return app