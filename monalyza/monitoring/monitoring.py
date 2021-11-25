import psutil
from . import buffer
from . import scheduler


class Monitoring(scheduler.Scheduler):

    def __init__(self, process, interval=None, buffer_size_mb=None):
        if buffer_size_mb is not None:
            self.buffer = buffer.Buffer(buffer_size_mb * 1000000)

        if interval is not None:
            self.scheduler = scheduler.Scheduler(interval)

        for proc in psutil.process_iter():
            if proc.name() == process or proc.pid == process:
                self.pid = proc.pid
                return

        raise ProcessLookupError("Could not find process with the given name",
                                 process)
        
    def run(self, read_memory=False, read_cpu=False):
        try:
            process = psutil.Process(self.pid)

            if read_memory:
                self.read_memory(process)

            if read_cpu:
                self.read_cpu(process)

        except psutil.NoSuchProcess:
            self.scheduler.cancel_scheduler()

        else:
            self.scheduler.schedule(self.run, read_memory=read_memory, 
                                    read_cpu=read_cpu)

    def read_memory(self, process=None):
        try: 
            if process is None:
                process = psutil.Process(self.pid)

            memory_info = process.memory_info()
            
        except psutil.NoSuchProcess as error:
            return error

        else:
            if hasattr(self, 'buffer'):
                self.buffer.append_to_buffer('Memory', memory_info)
            
            else:
                return memory_info

    def read_cpu(self, process=None):
        try: 
            if process is None:
                process = psutil.Process(self.pid)

            cpu_percent = process.cpu_percent(interval=1)
            
        except psutil.NoSuchProcess as error:
            return error

        else:
            if hasattr(self, 'buffer'):
                self.buffer.append_to_buffer('CPU', cpu_percent)
            
            else:
                return cpu_percent

