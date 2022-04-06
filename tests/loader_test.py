import unittest
from unittest.mock import patch
from monalyza.analysis import loader


class TestLoader(unittest.TestCase):

    def setUp(self):
        print('setUp')
        self.csv_file = 'measurements_output.csv'

    @patch('pandas.read_csv')
    def test_get_dataframe_from_csv(self, mock_read_csv):
        print('test1')
        loader.get_dataframe_from_csv(self.csv_file)
        mock_read_csv.assert_called_once_with(self.csv_file)

    @patch('pandas.read_csv', 'pandas.dataframe.groupby',
           'pandas.dataframe.sum')
    def test_combine_csv_measurements(self, mock_read_csv, mock_groupby,
                                      mock_sum):
        print('test2')
        group = 'time'
        loader.combine_csv_measurements(self.csv_file, group)
        mock_read_csv.assert_called_once_with(self.csv_file)
        mock_groupby.assert_called_once(group)
        mock_sum.assert_called_once()
