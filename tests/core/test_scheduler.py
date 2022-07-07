import time
import unittest
from unittest.mock import MagicMock, patch
from mona.core.scheduler import Scheduler


class TestScheduler(unittest.TestCase):
    """Test the correctness of scheduler."""

    def setUp(self):
        """Setup scheduler with interval of 1 second for testing"""
        self.interval = 1
        self.scheduler = Scheduler(self.interval)

    @patch('threading.Timer')
    @patch('threading.Timer.cancel')
    def test_scheduling_with_none(self, mock_timer, mock_cancel):
        """Test scheduling without a task"""
        self.scheduler.schedule(None)
        self.assertFalse(self.scheduler.running)
        mock_timer.assert_not_called()
        
        self.scheduler.cancel_scheduler()
        mock_cancel.assert_not_called()
        
        self.scheduler.running = True
        self.scheduler.cancel_scheduler()
        mock_cancel.assert_not_called()

    @patch('threading.Timer.cancel')
    def test_scheduled_function(self, mock_cancel):
        """Test scheduling with a task"""
        mock_monitoring_function = MagicMock()
        self.scheduler.schedule(mock_monitoring_function)
        self.assertTrue(self.scheduler.running)
        mock_monitoring_function.assert_not_called()

        time.sleep(self.interval + 1)

        mock_monitoring_function.assert_called_once()

        self.scheduler.cancel_scheduler()
        mock_cancel.assert_called_once()
