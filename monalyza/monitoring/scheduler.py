import threading
import logging


class Scheduler:
    """ Schedules a task to repeat periodically.
        It can only have one scheduled task. """
    def __init__(self, interval):
        """ Initialize the scheduler with desired interval. """
        logging.info('Initializing scheduler with interval %s.', interval)
        self.scheduled_timer = None
        self.running = False
        self.interval = interval

    def schedule(self, task, **params):
        """ Schedule the task to be executed. """
        logging.info('Scheduling the next run.')
        if task is not None:
            self.running = True
            self.scheduled_timer = threading.Timer(self.interval, task, params)
            self.scheduled_timer.start()
            logging.info('Scheduled the next run successfully.')

    def cancel_scheduler(self):
        """ Cancel all scheduled tasks. """
        logging.info('Cancelling the scheduled_timer.')
        if self.scheduled_timer is not None and self.running:
            self.running = False
            self.scheduled_timer.cancel()
            logging.info('Timer cancelled.')
