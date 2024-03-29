import unittest
from unittest.mock import patch
from mona.core import single_process_monitoring as spm


@unittest.skip('Monitoring is expected to fail')
class TestMonitoring(unittest.TestCase):

    class MockProc:
        pid = 1234

        def name(self):
            return 'FakeProcess'

    def setUp(self):
        self.patcher = patch('psutil.process_iter',
                             return_value=[self.MockProc()]).start()
        self.monitoring = spm.SingleProcessMonitoring('FakeProcess', 1,
                                                      1000000, 'test_output')

    def tearDown(self):
        self.patcher.stop()

    def test_proc_exist(self):
        # I do not know if this is the best way of testing the pid.
        self.assertEqual(self.monitoring.pid,
                         self.patcher.return_value[0].pid)

    def test_proc_not_exist(self):
        self.patcher.return_value = []
        self.assertRaises(
            ProcessLookupError, Monitoring, 1, 'invalid_proc_name')

    @patch('mona.monitoring.scheduler.Scheduler.schedule')
    @patch('psutil.Process')
    def test_run_pid_valid(self, mock_psutil_process, mock_schedule):
        self.monitoring.run_repeatedly()
        mock_psutil_process.assert_called_once_with(self.MockProc.pid)
        mock_schedule.assert_called_once()

    @patch('mona.monitoring.scheduler.Scheduler.cancel_scheduler')
    def test_run_pid_invalid(self, mock_cancel):
        self.monitoring.run_repeatedly()
        mock_cancel.assert_called_once()
