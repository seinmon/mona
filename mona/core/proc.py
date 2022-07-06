from __future__ import annotations
import logging
import psutil


def get_pid_of_process(process: str | int) -> int:
    """
    Find and return the defined process using its name or pid

    Note: This method is only tested for normal processes. Deamons are still
    not tested.

    - Parameters:
        -- process: an string or integer value representing the pid or process
        name

    - Returns: if the pid or process name exists, returns the pid

    - Raises: 
        -- ProcessLookupError: If pid or process name does not exists
    """
    for proc in psutil.process_iter():
        if process in (proc.name(), proc.pid):
            logging.debug('Process found.')
            return proc.pid

    raise ProcessLookupError('Could not find process', process)
