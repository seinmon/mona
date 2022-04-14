import logging
import psutil


def get_pid_of_process(process: str | int) -> int:
    """Find and return the defined process using its name or pid."""
    if isinstance(process, str) and process.isdigit():
        process = int(process)

    logging.debug('Iterating over processes to find %s.', process)
    for proc in psutil.process_iter():
        if process == proc.name() or process ==  proc.pid:
            logging.debug('Process found.')
            return proc.pid

    raise ProcessLookupError('Could not find process', process)
