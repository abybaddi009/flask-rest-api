import os
from multiprocessing import Lock

import requests

from .database import db
from .models import Iris


class SingletonMeta(type):
    """
    Multiprocessing-safe implementation of Singleton.
    """

    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


def number_of_lines(filename):
    """
    Returns the number of lines in a file excluding the header
    """
    with open(filename, "r") as f:
        i = 0
        for i, _ in enumerate(f):
            pass
        return i


class FetchCSV(metaclass=SingletonMeta):
    @classmethod
    def download_csv_from_url(cls, CSV_URL):
        """
        Fetches and streams the CSV to local storage and simultaneously inserts into the DB.
        If the remote has more rows, the newer rows are appended to local file.
        """
        FILENAME = os.path.split(CSV_URL)[1]

        db_row_count = db.session.query(db.func.count(Iris.id)).scalar()
        file_row_count = 0
        if os.path.exists(FILENAME):
            file_row_count = number_of_lines(FILENAME)

        with open(FILENAME, "ab") as f, requests.get(CSV_URL, stream=True) as r:
            headers = []
            for index, line in enumerate(r.iter_lines()):
                if index == 0:
                    headers = line.decode().split(",")

                if index < file_row_count:
                    continue
                else:
                    if index > db_row_count:
                        iris = Iris(
                            **{
                                key: value
                                for key, value in zip(headers, line.decode().split(","))
                            }
                        )
                        db.session.add(iris)
                        db.session.commit()
                f.write(line + "\n".encode())
