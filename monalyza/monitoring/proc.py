import logging
import psutil


def get_pid_of_process(process: str | int) -> int:
    """Find and return the defined process using its name or pid."""
    for proc in psutil.process_iter():
        if process in (proc.name(), proc.pid):
            logging.debug('Process found.')
            return proc.pid

    raise ProcessLookupError('Could not find process', process)
