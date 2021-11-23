import threading


class Scheduler:
    def __init__(self, interval):
        self.scheduled_timer = None 
        self.running = False
        self.interval = interval

    def schedule(self, monitoring_function):
        if monitoring_function is not None:
            self.running = True
            self.scheduled_timer = threading.Timer(self.interval, monitoring_function)
            self.scheduled_timer.start()

    def cancel_scheduler(self):
        if self.scheduled_timer is not None and self.running:
            self.running = False
            self.scheduled_timer.cancel()

