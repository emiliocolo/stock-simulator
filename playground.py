# log_base
from log_base.formatting import *
from log_base.logger import *
from log_base.timer import *

# stock service
from stock_service.server import *
from stock_service.tickers import *

if __name__ == "__main__" and __package__ is None:
    log = setup_logger(debug_level='WARNING')
    log.info("Python playground")
    #log.info("Python version: %s" % get_python_version())
    #log.info("Pandas version: %s" % get_library_version('pandas'))
    #log.info("Numpy version: %s" % get_library_version('numpy'))
   # log.info("OpenCV version: %s" % get_library_version('cv2'))

    with Timer() as t:
        log.info("Starting process")
        # Add here the code -----
        # Start the REST API Server
        app = create_server()

        # Create Ticker Simulator
        ticker_simulator = Ticker("SEOULAI", log, app)
        ticker_simulator.start()

        app.run(debug=True)

        # End of code -----
    log.info("Process finished in %.5f seconds" % t.interval)
