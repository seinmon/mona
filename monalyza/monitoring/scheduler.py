import threading
import logging


class Scheduler:
    def __init__(self, interval):
        logging.info('Initializing scheduler with interval %s.', interval)
        self.scheduled_timer = None 
        self.running = False
        self.interval = interval

    def schedule(self, monitoring_function, **params):
        logging.info('Scheduling the next run.')
        if monitoring_function is not None:
            self.running = True
            self.scheduled_timer = threading.Timer(self.interval,
                                                   monitoring_function,
                                                   params)
            self.scheduled_timer.start()
            logging.info('Scheduled the next run successfully.')

    def cancel_scheduler(self):
        logging.info('Cancelling the scheduled_timer.')
        if self.scheduled_timer is not None and self.running:
            self.running = False
            self.scheduled_timer.cancel()
            logging.info('Timer cancelled.')

