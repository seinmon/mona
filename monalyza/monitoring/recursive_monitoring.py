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
                self.get_children()
            except psutil.NoSuchProcess:
                return

    def get_children(self):
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
                
