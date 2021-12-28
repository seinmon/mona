import logging
import threading
import psutil
from monalyza.monitoring import proc, single_process_monitoring as spm


class RecursiveMonitoring(threading.Thread, proc.Proc):

    def __init__(self, process, interval, buffer):
        try:
            proc.Proc.__init__(self, process)
        except ProcessLookupError:
            raise

        threading.Thread.__init__(self)
             
        logging.debug('Initializing recursive monitoring.')
        self.interval = interval
        self.buffer = buffer
        self.processes = []

    def run(self):
        logging.debug('Running RecursiveMonitoring.')
        
        try: 
            self.processes.append(psutil.Process(self.pid))
        except psutil.NoSuchProcess:
            raise

        monitor = spm.SingleProcessMonitoring(self.pid,
                                              self.interval,
                                              self.buffer)
        threading.Thread(target=monitor.run_repeatedly,
                         kwargs={'read_memory':True, 'read_cpu':True}).start()

        while True:
            try:
                self.monitor_children()
            except psutil.NoSuchProcess:
                logging.debug('Main process is finished.')
                return

    def monitor_children(self):
        try:
            children = psutil.Process(self.pid).children()

        except psutil.NoSuchProcess:
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
                        kwargs={'read_memory':True, 'read_cpu':True}
                    ).start()

            for process in self.processes:
                if process not in children:
                    self.processes.remove(process)
                    logging.debug('%s is dead, and removed from processes list',
                                 process)
                
