import logging
import pandas as pd
import matplotlib


class Loader:

    def __init__(self, measurements):
        logging.debug('Initializing loader.')
        self.data = pd.read_csv(measurements)

        # Keep this empty, and populate when its needed.
        self.all_pids = []

    def get_all_columns(self):
        """ Get the column names.
            It is useful to see which resources are monitored. """
        print('columns are:')
        print(self.data.columns)
        print('indexes are: ')
        print(self.data.index)


    # def get_all_pids(self):
    #     """ Getting all measured pids. """
    #     logging.debug('Getting all measured pids.')
    #     for pid in self.data['pid']:
    #         if pid not in self.all_pids:
    #             self.all_pids.append(pid)

    def combine_measurements(self):
        return self.data.groupby('time')[self.data.columns[2:]].sum()



if __name__ == '__main__':
    loader = Loader('measurements_output.csv')
    print(loader.combine_measurements())
