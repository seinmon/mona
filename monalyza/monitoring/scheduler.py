import threading


class Scheduler:
    def __init__(self, interval):
        print("Initializing the scheduler...")
        self.scheduled_timer = None
        self.running = False
        self.interval = interval

    def schedule(self, monitoring_function):
        print("PID is valid: Scheduling...")
        self.running = True
        self.scheduled_timer = threading.Timer(self.interval, monitoring_function).start()

    def cancel_scheduler(self):
        print("PID is invalid: Cancelling existing timers...")
        if self.scheduled_timer is not None and self.running:
            self.running = False
            self.scheduled_timer.cancel()
            self.scheduled_timer = None
            print("Timer cancelled.")
