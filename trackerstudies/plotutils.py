import matplotlib.pyplot as plt


def plot_matrix(matrix, *args, **kwargs):
    fig, ax = plt.subplots()
    plt.imshow(matrix)
    _post_process_plot(*args, **kwargs)


def plot_line(x, y, *args, **kwargs):
    fig, ax = plt.subplots()
    plt.plot(x, y)
    _post_process_plot(*args, **kwargs)


def _post_process_plot(title=None, xlabel=None, ylabel=None, show=False, save=None):
    if title:
        plt.title(title)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    if save:
        file_name = save
        save_plot(file_name)
    if show:
        plt.show()


def save_plot(file_name):
    plt.savefig(file_name)


def save_with_default_name(save, default):
    if save:
        if save is True:
            file_name = default
        else:
            file_name = save
        save_plot(file_name)
