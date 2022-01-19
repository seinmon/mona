from os import path
import sys
import logging
# import argparse
from monalyza.monitoring import buffer, recursive_monitoring
import monalyza.monitoring.single_process_monitoring as smp


def initialize_logger(level=logging.INFO, verbose_print=False):
    """ Initialize logger with specified level. """
    logging.basicConfig(
        filename=path.join(path.expanduser('~'), '.monalyza.log'),
        encoding='utf-8',
        level=level,
        format='%(asctime)s [%(levelname)s]'
        '[%(threadName)s/%(thread)d] %(message)s')

    if verbose_print:
        logging.getLogger().addHandler(logging.StreamHandler())


def main():
    """ Starting point of the application. """
    initialize_logger()
    logging.info('Starting...')
    process = sys.argv[1]

    # TODO: Change recursive flag to a command option
    recursive = True
    output_buffer = buffer.Buffer(12000000, 'measurements_output.csv')

    try:
        if recursive:
            monitor = recursive_monitoring.RecursiveMonitoring(process,
                                                               1,
                                                               output_buffer)

        else:
            monitor = smp.SingleProcessMonitoring(process,
                                                  interval=1,
                                                  buffer=output_buffer)

    except ProcessLookupError as p_err:
        logging.error(repr(p_err))
        return 1

    else:
        if recursive:
            monitor.start()

        else:
            monitor.run_repeatedly(True, True)

        return 0
