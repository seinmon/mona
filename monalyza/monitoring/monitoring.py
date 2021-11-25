import psutil
from . import scheduler


class Monitoring(scheduler.Scheduler):

    def __init__(self, interval, proc_name):
        self.scheduler = scheduler.Scheduler(interval)

        for proc in psutil.process_iter():
            if proc.name() == proc_name:
                self.pid = proc.pid
                return

        raise ProcessLookupError("Could not find process with the given name",
                                 proc_name)
        
    def run(self, read_memory=False, read_cpu=False):
        try:
            process = psutil.Process(self.pid)

            if read_memory:
                print(process.memory_info()) 

            if read_cpu:
                print(process.cpu_percent(interval=1))

        except psutil.NoSuchProcess:
            self.scheduler.cancel_scheduler()

        else:
            self.scheduler.schedule(self.run, read_memory=read_memory, read_cpu=read_cpu)

    # def read_memory(self, process):
    #     try: 
    #         print(process.memory_info()) 

    #     except psutil.NoSuchProcess:
    #         pass

    # def read_cpu(self, process):
    #     try: 
    #         print(process.cpu_percent(interval=1))

    #     except psutil.NoSuchProcess:
    #         pass
