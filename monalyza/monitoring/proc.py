import logging
import psutil


def get_pid_of_process(process):
    """ Find and return the desired process. """

    logging.debug('Iterating over processes to find %s.', process)
    for proc in psutil.process_iter():
        if proc.name() in process or proc.pid in process:
            logging.debug('Process found.')
            return proc.pid

    raise ProcessLookupError('Could not find process', process)
