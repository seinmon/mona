import psutil
import logging


class Proc:

    def __init__(self, process):
        logging.debug('Iterating over processes to find %s.', process)
        for proc in psutil.process_iter():
            if proc.name() == process or proc.pid == process:
                logging.debug('Process found.')
                self.pid = proc.pid
                return

        raise ProcessLookupError('Could not find process', process)
