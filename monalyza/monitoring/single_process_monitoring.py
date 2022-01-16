import logging
import time
import psutil
from monalyza.monitoring import scheduler, proc

class SingleProcessMonitoring(proc.Proc):

    def __init__(self,
                 process,
                 interval=None,
                 buffer=None,
                 hide_headers=False):
        try:
            proc.Proc.__init__(self, process)

        except ProcessLookupError:
            raise

        self.first_run = not hide_headers

        logging.debug('Initializing single process monitoring.')
        self.buffer = buffer

        if interval is not None:
            self.scheduler = scheduler.Scheduler(interval)

        else:
            self.scheduler = None

    def run_repeatedly(self, read_memory=False, read_cpu=False):
        """ Repeat measurements periodically. """
        
        if self.scheduler is None or self.buffer is None:
            raise UnboundLocalError(
                'Unexpectped value:',
                self.buffer,
                self.scheduler,
                'Either interval or buffer_size_mb is missing')

        try:
            resource_info = self.read_resource(read_memory, read_cpu)

        except psutil.NoSuchProcess:
            self.scheduler.cancel_scheduler()
            self.buffer.write_data()

        else:
            if self.first_run:
                headers = None

                if read_memory and read_cpu:
                    headers = ('pid', 'time', 'memory', 'cpu')

                elif read_memory:
                    headers = ('pid', 'time', 'memory')

                elif read_cpu:
                    headers = ('pid', 'time', 'cpu')

                self.buffer.append_to_buffer(headers)
                self.first_run = False

            self.buffer.append_to_buffer(resource_info)
            self.scheduler.schedule(self.run_repeatedly,
                                    read_memory=read_memory, 
                                    read_cpu=read_cpu)

    def read_resource(self, read_memory=False, read_cpu=False):
        """ Measure resources only once. It is used inside run_repeatedly. """
        resource_info = None

        try: 
            process = psutil.Process(self.pid)

            if read_memory and read_cpu:
                resource_info = (process.pid,
                                 self.generate_timestamp(),
                                 process.memory_info()[0],
                                 process.cpu_percent(interval=0.1))

            elif read_memory:
                resource_info = (process.pid,
                                 self.generate_timestamp(),
                                 process.memory_info()[0])

            elif read_cpu:
                resource_info = (process.pid,
                                 self.generate_timestamp(),
                                 process.cpu_percent(interval=1))
            
        except psutil.NoSuchProcess: 
            raise

        else:
            return resource_info
    
    def generate_timestamp(self):
        """ Return current time in miliseconds """
        # This method does not return the exact time
        return int(time.time() * 1000)
