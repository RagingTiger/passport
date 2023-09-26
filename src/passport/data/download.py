"""Utils for downloading passport data."""
import tarfile
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin
from urllib.request import urlretrieve


GITHUB_URL = "https://github.com"
RELEASES_URL = urljoin(GITHUB_URL, "RagingTiger/passport/releases/download/")
DATASET_URLS = {
    "passportindex_2023": RELEASES_URL + "v0.0.1/passportindex_2023.tar.gz",
}


def _extract(in_path: Path, out_path: Path) -> Path:
    """Extract contents of downloaded file to output directory."""
    # open tarfile
    with tarfile.open(str(in_path)) as tar:
        # extract to output dir
        tar.extractall(path=str(out_path))

    # return output path
    return out_path


def _download(url: str, file_path: Optional[str] = None) -> Path:
    """Downloads data from a given URL to a given path."""
    # get hosted filed from URL, download to
    download_path, _ = urlretrieve(url, file_path)

    # return download path
    return Path(download_path)


def _resolve_url(name_path: str) -> str:
    """Takes in a given path/url/dataset_name and returns the appropriate format."""
    # check if http/https
    if "http" in name_path:
        # nothing to do it's ready to use
        pass

    elif "file://" in name_path:
        # also nothing to do
        pass

    elif Path(name_path).exists():
        # convert to path object
        file_path = Path(name_path)

        # now create file url
        name_path = "file://" + str(file_path.resolve())

    else:
        # make sure name is in
        assert (
            name_path in DATASET_URLS
        ), f"{name_path} is not among datasets available: {DATASET_URLS.keys()}"

        # get url for dataset
        name_path = DATASET_URLS[name_path]

    # resolved
    return name_path


def get_data(dataset: str, out_path: str) -> str:
    """Resolves the URL for a given dataset name and attempts to download/extract."""
    # get url from name or return otherwise
    data_url = _resolve_url(dataset)

    # now download and get path to dataset
    download_file_path = _download(data_url)

    # check if compressed
    if tarfile.is_tarfile(download_file_path):
        # power up path
        out_pathlib_path = Path(out_path)

        # check data dir exists
        if not out_pathlib_path.exists():
            # make it
            out_pathlib_path.mkdir(parents=True)

        # need to extract
        final_path = str(_extract(download_file_path, out_pathlib_path))
    else:
        # just get download path
        final_path = str(download_file_path)

    # now extract and get path to folder
    return final_path
