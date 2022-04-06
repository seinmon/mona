""" Loads csv file, and performs a certain action on its content. """
import logging
import pandas as pd


def get_dataframe_from_csv(csv):
    """ Create dataframe based on the measurement values in csv file. """
    logging.debug("Creating dataframe from %s file", csv)
    return pd.read_csv(csv)


def combine_csv_measurements(csv, group):
    """ Combine measurements that have similar values in a certain column. """
    data = get_dataframe_from_csv(csv)
    logging.debug("Merging values based on %s column", group)
    return data.groupby(group)[data.columns[2:]].sum()


if __name__ == '__main__':
    print(combine_csv_measurements('measurements_output.csv', 'time'))
