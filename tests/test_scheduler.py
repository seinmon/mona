import unittest
from unittest.mock import MagicMock
import threading
import time
from monalyza.monitoring.scheduler import Scheduler


class TestScheduler(unittest.TestCase):
    def setUp(self):
        self.interval = 1
        self.scheduler = Scheduler(self.interval)

    def test_initializer(self):
        self.assertFalse(self.scheduler.running)
        self.assertEqual(self.scheduler.interval, self.interval)
        self.assertIsNone(self.scheduler.scheduled_timer)

    def test_scheduling_with_none(self):
        threading.Timer = MagicMock()
        self.scheduler.schedule(None)
        self.assertFalse(self.scheduler.running)
        threading.Timer.assert_not_called()

    def test_scheduling_with_function(self):
        threading.Timer = MagicMock()        
        monitoring_function = ()
        self.scheduler.schedule(monitoring_function)
        self.assertTrue(self.scheduler.running)
        threading.Timer.assert_called_once_with(self.interval, 
                                                monitoring_function)
        
    def test_scheduled_function(self):
        monitoring_function = MagicMock()
        self.scheduler.schedule(monitoring_function)
        
        self.assertTrue(self.scheduler.running)
        monitoring_function.assert_not_called()

        time.sleep(self.interval + 1)

        monitoring_function.assert_called_once()

    def test_cacel_not_running_not_scheduled(self):
        threading.Timer.cancel = MagicMock()
        self.scheduler.cancel_scheduler()
        threading.Timer.cancel.assert_not_called()

    def test_cancel_not_running_scheduled(self):
        threading.Timer.cancel = MagicMock()
        self.scheduler.scheduled_timer = MagicMock() 
        self.scheduler.cancel_scheduler()
        threading.Timer.cancel.assert_not_called()

    def test_cancel_runnin_not_scheduled(self):
        threading.Timer.cancel = MagicMock()
        self.scheduler.running = True 
        self.scheduler.cancel_scheduler()
        threading.Timer.cancel.assert_not_called()

    def test_cancel(self):
        threading.Timer.cancel = MagicMock()
        self.scheduler.running = True 
        self.scheduler.scheduled_timer = MagicMock() 
        self.scheduler.cancel_scheduler()
        threading.Timer.cancel.assert_not_called()

