import logging
import psutil


def execute_process(command: list[str]) -> int:
    """Execute the process that needs to be monitored."""
    proc = psutil.Popen(command)
    return proc.pid


def get_pid_of_process(process: list[str] | str | int) -> int:
    """Find and return the defined process using its name or pid."""
    if isinstance(process, list):
        process = process[0]

    logging.debug('Iterating over processes to find %s.', process)
    for proc in psutil.process_iter():
        if process in (proc.name(), proc.pid):
            logging.debug('Process found.')
            return proc.pid

    raise ProcessLookupError('Could not find process', process)
