from __future__ import annotations
import threading
import logging


class Scheduler:
    """Schedule a single task to repeat periodically"""
    def __init__(self, interval: float) -> None:
        """
        Schedule a single task to repeat periodically

        - Parameters:
            -- interval: interval of executing the scheduled task
        """
        logging.info('Initializing scheduler with interval %s.', interval)
        self.scheduled_timer = None
        self.running = False
        self.interval = interval

    # TODO: Add type annotations
    def schedule(self, task, **params) -> None:
        """
        Schedule a function to be executed with **params as parameters

        - Parameters:
            -- task: the function to be executed
            -- **params: a list of parameters to use in the task
        """
        logging.info('Scheduling the next run.')
        if task is not None:
            self.running = True
            self.scheduled_timer = threading.Timer(self.interval, task, params)
            self.scheduled_timer.start()
            logging.info('Scheduled the next run successfully.')

    def cancel_scheduler(self) -> None:
        """Cancel scheduled tasks"""
        logging.info('Cancelling the scheduled_timer.')
        if self.scheduled_timer is not None and self.running:
            self.running = False
            self.scheduled_timer.cancel()
            logging.info('Timer cancelled.')
