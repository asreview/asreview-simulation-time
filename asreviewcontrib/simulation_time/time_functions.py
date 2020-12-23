import matplotlib.pyplot as plt
from asreview.state.utils import open_state
from datetime import datetime
import os


def unpack_plt_kwargs(**kwargs):
    try:
        plt.title(kwargs['title'])
    except KeyError:
        pass

    try:
        plt.xlabel(kwargs['xlabel'])
    except KeyError:
        pass

    try:
        plt.ylabel(kwargs['ylabel'])
    except KeyError:
        pass


def create_time_list(state_fp):
    """Create a list of creation times from a state file.

    Arguments
    ----------
    state_fp: str
        Path to state file

    Returns
    -------
    list
        List of creation time of each query in the state_file results, in
        datetime format '%Y-%m-%d %H:%M:%S.%f'. Note that the first entry is
        the creation time of the 0'th query, not the 'start_time' of the state
        file. Similarly, the last entry is the creation time of the last query,
        not the 'end_time' of the state file.
    """
    time_list = []
    with open_state(state_fp) as state:
        for i in range(len(state.f['results'])):
            time = state.f[f'results/{i}'].attrs['creation_time']
            time = time.decode('UTF-8')
            time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
            time_list.append(time)
    return time_list


def plot_time_from_start(fp, **kwargs):
    """Plot the time at which the queries where made, relative to the start.

    Arguments
    ----------
    fp: str
        Path to state file or directory with state files.

    Returns
    -------
    Plot of the creation time of the current query, minus the creation time of
    the 0'th query. On the x-axis we have the
    query index. On the y-axis we have the number of seconds.
    """
    if os.path.isfile(fp):
        files = [fp]
    else:
        files = [os.path.join(fp, file) for file in os.listdir(fp)]
    for file in files:
        time_list = create_time_list(file)
        time_list = [(time - time_list[0]).total_seconds()
                     for time in time_list]
        plt.plot(time_list)
    unpack_plt_kwargs(**kwargs)
    plt.show()


def plot_time_between_queries(fp, from_one=True, **kwargs):
    """Plot the time between queries.

    Arguments
    ----------
    fp: str
        Path to state file or directory with state files.
    from_one: bool
        If True, start from the 1'st query instead of the 0'th query. The time
        between the 0'th query and the 1'st query has different behaviour
        than between the other queries.

    Returns
    -------
    Plot of the time between the current query and the next query. On the
    x-axis we have the query index. On the y-axis we have the time in seconds.
    """
    if os.path.isfile(fp):
        files = [fp]
    else:
        files = [os.path.join(fp, file) for file in os.listdir(fp)]
    for file in files:
        time_list = create_time_list(file)
        start = int(from_one)
        time_list = [(time_list[i+1] - time_list[i]).total_seconds()
                     for i in range(start, len(time_list)-2)]
        plt.plot(time_list)
    unpack_plt_kwargs(**kwargs)
    plt.show()


if __name__ == '__main__':

    fp = 'test_data/dif_model_runs/ace_rf.h5'
    plot_time_between_queries(fp,
                              from_one=True,
                              **{'title': 'Model: Random Forest',
                                 'xlabel': 'Queries',
                                 'ylabel': 'Time to next query (seconds)'})
    plot_time_from_start(fp,
                         **{'title': 'Model: Random Forest',
                            'xlabel': 'Queries',
                            'ylabel': 'Time from start (seconds)'})
