from os import path
import sys
import logging
from monalyza.monitoring import buffer, recursive_monitoring
import monalyza.monitoring.single_process_monitoring as smp


def initialize_logger(level: int = logging.DEBUG,
                      verbose_print: bool = False) -> None:
    """Initialize logger with the specified logging level.
    If you want to print logs while executing, set verbose_print to true."""
    logging.basicConfig(
        filename=path.join(path.expanduser('~'), '.monalyza.log'),
        encoding='utf-8',
        level=level,
        format='%(asctime)s [%(levelname)s]'
        '[%(threadName)s/%(thread)d] %(message)s')

    if verbose_print:
        logging.getLogger().addHandler(logging.StreamHandler())


def main() -> int:
    """Starting point of the application."""

    initialize_logger()
    logging.info('Starting...')
    command = sys.argv[1]

    # TODO: Change recursive flag to a command option
    recursive = True
    output_buffer = buffer.Buffer(12000000, 'measurements_output.csv')

    try:
        if recursive:
            monitor = recursive_monitoring.RecursiveMonitoring(command,
                                                               1,
                                                               output_buffer)

        else:
            monitor = smp.SingleProcessMonitoring(command,
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
