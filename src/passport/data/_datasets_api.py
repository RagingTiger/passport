"""Private module that implements the API for different passport datasets."""
import os
import pathlib

import pandas

from .download import get_data


def passport_dataframe(dataset: str) -> pandas.DataFrame:
    """Loads the supplied dataset into a Pandas DataFrame."""
    # create output path
    data_dir = pathlib.Path(os.getcwd()) / ".passport"

    # download data
    data_file = pathlib.Path(get_data(dataset, str(data_dir)))

    # check if dir
    if data_file.is_dir():
        # get contents of directory
        contents = next(data_file.glob("**/*.csv"))

        # modify path
        data_file = data_file / contents

    # check data is indeed csv
    assert "csv" in data_file.suffix

    # get data frame
    return pandas.read_csv(data_file)
