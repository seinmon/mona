import psutil
from monitoring import scheduler


class Monitoring(scheduler.Scheduler):

    def __init__(self, interval, proc_name):
        super().__init__(interval)

        for proc in psutil.process_iter():
            if proc.name() == proc_name:
                self.pid = proc.pid
                return

        print("Process not found")
        quit(1)

    def memory(self):
        try:
            memory_info = psutil.Process(self.pid).memory_info()

        except psutil.NoSuchProcess:
            super().cancel_scheduler()

        else:
            print(memory_info)
            super().schedule(self.memory)

    def cpu(self):
        try:
            cpu_load = psutil.Process(self.pid).cpu_percent(interval=1)

        except psutil.NoSuchProcess:
            super().cancel_scheduler()

        else:
            print(cpu_load)
            super().schedule(self.cpu)
