import logging
import pandas as pd


class Loader:
    """ Load the measurements, and prepare values for analysis. """

    def __init__(self, measurements):
        """ Create dataframe based on the measurement values in csv file. """
        logging.debug("Creating dataframe from %s file", measurements)
        self.data = pd.read_csv(measurements)

    def combine_values_by(self, group):
        """ Combine measurements that have similar values in a certain column.
        """
        logging.debug("Merging values based on %s column", group)
        return self.data.groupby(group)[self.data.columns[2:]].sum()

    def get_column(self, column):
        """ Get the values in a certain column as list. """
        return self.data.loc[:, column]

    def combine_and_get_column(self, group, column):
        """ Combine measurements that have similar values in a certain column,
        then return a column. """
        data = self.combine_values_by(group)
        return data.loc[:, column]
