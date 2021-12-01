from os import path
import sys
import logging
# import argparse
from monalyza.monitoring import monitoring


def initialize_logger(level=logging.WARNING):
    logging.basicConfig(
        filename=path.join(path.expanduser('~'), '.monalyza.log'),
        encoding='utf-8',
        level=level,
        format=
        '%(asctime)s [%(levelname)s] [%(threadName)s/%(thread)d] %(message)s')

    logging.getLogger().addHandler(logging.StreamHandler())


def main():
    logging.info('Starting...')
    initialize_logger()
    process = sys.argv[1]

    try: 
        monitor = monitoring.Monitoring(process,
                                        interval=1,
                                        buffer_size=12000000)

    except ProcessLookupError as p_err:
        logging.error(repr(p_err))
        return 1
        
    else:
        monitor.run_repeatedly(True, True)
        return 0

