import sys
import logging
from scipy import stats
# from monalyza.analysis import loader
import loader


def kruskal(*args):
    """ Compute Kruskal Wallis for 2 or more measurements. """
    logging.debug("Computing Kruskal Wallis")
    measurements = []

    for argument in args[0]:
        loaded_data = loader.Loader(argument)
        measurements.append(loaded_data.combine_and_get_column('time', 'cpu'))

    return stats.kruskal(*measurements)


if __name__ == '__main__':
    print(kruskal(sys.argv[1:]))
