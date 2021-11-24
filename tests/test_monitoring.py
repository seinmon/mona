import unittest
from unittest.mock import MagicMock, patch
from monalyza.monitoring.monitoring import Monitoring


class TestMonitoring(unittest.TestCase):

    class MockProc:
        pid = 1234

        def name():
            return 'FakeProcess'


    @patch('psutil.process_iter', return_value=[MockProc])
    def test_proc_exist(self, mock_process_iter):
        
        try:
            monitoring = Monitoring(1, "FakeProcess")

        except ProcessLookupError:
            self.fail("Failed to instantiate monitoring with FakeProcess")

        else:
            # I do not know if this is the best way of testing the pid.
            self.assertEqual(
                monitoring.pid, mock_process_iter.return_value[0].pid)

    def test_proc_not_exist(self):
        self.assertRaises(
            ProcessLookupError, Monitoring, 1, "invalid_proc_name")

    # def test_memory_pid_valid(self):
    #     pass

    # def test_memory_pid_invalid(self):
    #     pass

    # def test_cpu_pid_valid(self):
    #     pass

    # def test_cpu_pid_invalid(self):
    #     pass
