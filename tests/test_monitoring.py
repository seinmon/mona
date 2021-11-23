import unittest
# from unittest.mock import MagicMock
from monalyza.monitoring import monitoring


class TestMonitoring(unittest.TestCase):

    def test_proc_exist(self):


    def test_proc_not_exist(self):
        self.assertRaises(ProcessLookupError, monitoring.Monitoring, 1, "invalid_proc_name")

    def test_memory_pid_valid(self):
        pass

    def test_memory_pid_invalid(self):
        pass

    def test_cpu_pid_valid(self):
        pass

    def test_cpu_pid_invalid(self):
        pass
