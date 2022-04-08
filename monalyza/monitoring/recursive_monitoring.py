import logging
import threading
import psutil
import monalyza.monitoring.single_process_monitoring as spm
from monalyza.monitoring import proc, scheduler


class RecursiveMonitoring(threading.Thread):
    """ Monitor a process and its children. """
    def __init__(self, process, interval, buffer):
        try:
            self.pid = proc.get_pid_of_process(process)

        # pylint: disable=try-except-raise
        except ProcessLookupError:
            raise

        threading.Thread.__init__(self)

        logging.info('Initializing recursive monitoring.')
        self.interval = interval
        self.buffer = buffer
        self.processes = []

    def run(self):
        """ Start a monitoring thread for the main process.
            Also check for the child processes. """
        logging.debug('Running RecursiveMonitoring.')
        child_scheduler = scheduler.Scheduler(0.01)

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

    def monitor_children(self):
        """ Starts a thread to monitor children of the main process. """
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
