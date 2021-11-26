import time
import psutil
from . import buffer
from . import scheduler


class Monitoring(scheduler.Scheduler):

    def __init__(self,
                 process,
                 interval=None,
                 buffer_size=None,
                 output_file=None):
        self.first_run = True

        if buffer_size is not None:
            if output_file is None:
                output_file = 'measurement_output.csv'
            self.buffer = buffer.Buffer(buffer_size, output_file)

        else:
            self.buffer = None

        if interval is not None:
            self.scheduler = scheduler.Scheduler(interval)

        else:
            self.scheduler = None

        for proc in psutil.process_iter():
            if proc.name() == process or proc.pid == process:
                self.pid = proc.pid
                return

        raise ProcessLookupError('Could not find process with the given name',
                                 process)
        
    def run(self, read_memory=False, read_cpu=False):
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
                    headers = ('time', 'memory', 'cpu')

                elif read_memory:
                    headers = ('time', 'memory')

                elif read_cpu:
                    headers = ('time', 'cpu')

                self.buffer.append_to_buffer(headers)
                self.first_run = False

            if resource_info is not None:
                self.buffer.append_to_buffer(resource_info)
            self.scheduler.schedule(self.run,
                                    read_memory=read_memory, 
                                    read_cpu=read_cpu)

    def read_resource(self, read_memory=False, read_cpu=False):
        resource_info = None

        try: 
            process = psutil.Process(self.pid)

            if read_memory and read_cpu:
                resource_info = (self.generate_timestamp(),
                                 process.memory_info()[0],
                                 process.cpu_percent(interval=1))

            elif read_memory:
                resource_info = (self.generate_timestamp(),
                                 process.memory_info()[0])

            elif read_cpu:
                resource_info = (self.generate_timestamp(),
                                 process.cpu_percent(interval=1))
            
        except psutil.NoSuchProcess as error:
            return error

        return resource_info
    
    def generate_timestamp(self):
        """ Return current time in seconds """
        return round(time.time())

