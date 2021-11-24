import unittest
from unittest.mock import MagicMock, patch 
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

    @patch('threading.Timer')
    def test_scheduling_with_none(self, mock_timer):
        self.scheduler.schedule(None)
        self.assertFalse(self.scheduler.running)
        mock_timer.assert_not_called()

    @patch('threading.Timer')
    def test_scheduling_with_function(self, mock_timer):
        self.scheduler.schedule(())
        self.assertTrue(self.scheduler.running)
        mock_timer.assert_called_once_with(self.interval, ())
        
    def test_scheduled_function(self):
        mock_monitoring_function = MagicMock()
        self.scheduler.schedule(mock_monitoring_function)
        self.assertTrue(self.scheduler.running)
        mock_monitoring_function.assert_not_called()

        time.sleep(self.interval + 1)

        mock_monitoring_function.assert_called_once()

    @patch('threading.Timer.cancel')
    def test_cacel_not_running_not_scheduled(self, mock_cancel):
        self.scheduler.cancel_scheduler()
        mock_cancel.assert_not_called()

    @patch('threading.Timer.cancel')
    def test_cancel_not_running_scheduled(self, mock_cancel):
        self.scheduler.cancel_scheduler()
        mock_cancel.assert_not_called()

    @patch('threading.Timer.cancel')
    def test_cancel_runnin_not_scheduled(self, mock_cancel):
        self.scheduler.running = True 
        self.scheduler.cancel_scheduler()
        mock_cancel.assert_not_called()

    @patch('threading.Timer.cancel')
    def test_cancel(self, mock_cancel):
        self.scheduler.running = True 
        self.scheduler.cancel_scheduler()
        mock_cancel.assert_not_called()

