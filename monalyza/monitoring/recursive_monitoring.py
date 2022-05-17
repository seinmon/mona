from __future__ import annotations
import logging
import threading
from typing import TYPE_CHECKING
import psutil
import monalyza.monitoring.single_process_monitoring as spm
from monalyza.monitoring import scheduler


if TYPE_CHECKING:
    from monalyza.monitoring.buffer import Buffer


class RecursiveMonitoring(threading.Thread):
    """Monitor a process and its children."""

    def __init__(self, pid: int, buffer: 'Buffer',
                 interval: float = 1, recursion_interval: float = 0.01,
                 recursion_time: int | None = None) -> None:
        self.pid = pid
        threading.Thread.__init__(self)

        logging.info('Initializing recursive monitoring.')
        self.interval = interval
        self.buffer = buffer

        self.recursion_interval = recursion_interval
        self.recursion_time = recursion_time
        self.processes = []

    # TODO: Add optional time limit for child monitoring.
    def run(self) -> None:
        """Start a monitoring thread for the main process,
        and check for its child processes."""
        logging.debug('Running RecursiveMonitoring.')
        child_scheduler = scheduler.Scheduler(self.recursion_interval)

        try:
            self.processes.append(psutil.Process(self.pid))
        except psutil.NoSuchProcess:
            logging.debug('Main process is finished.')
            raise

        monitor = spm.SingleProcessMonitoring(self.pid,
                                              self.interval,
                                              self.buffer)
        threading.Thread(target=monitor.run_repeatedly,
                         kwargs={'read_memory': True,
                                 'read_cpu': True}).start()

        try:
            child_scheduler.schedule(self.monitor_children())
        except psutil.NoSuchProcess:
            logging.info('No longer monitoring for children.')
            child_scheduler.cancel_scheduler()
            return

    def monitor_children(self) -> None:
        """Starts a thread to monitor children of the main process."""
        try:
            children = psutil.Process(self.pid).children()

        except psutil.NoSuchProcess:
            logging.info('Cannot find children - Main process is finished.')
            raise

        else:
            for child_proc in children:
                if child_proc not in self.processes:
                    logging.debug('New child process %s to monitor.',
                                  child_proc)
                    self.processes.append(child_proc)
                    monitor = spm.SingleProcessMonitoring(child_proc.pid,
                                                          self.interval,
                                                          self.buffer,
                                                          True)
                    threading.Thread(
                        target=monitor.run_repeatedly,
                        kwargs={'read_memory': True, 'read_cpu': True}
                    ).start()

            for process in self.processes:
                if process not in children:
                    logging.debug('Removing %s from processes list', process)
                    self.processes.remove(process)
