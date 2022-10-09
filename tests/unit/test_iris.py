import os

from app.dataset import FetchCSV
from app.models import Iris


def test_iris_columns_are_float(new_irisrow):
    """
    GIVEN a new Iris dataset row
    WHEN the Iris model is created
    THEN the values for the columns must be float
    """
    assert new_irisrow.species == 'random'
    for column in Iris.column_names():
        assert type(getattr(new_irisrow, column)) == float


def test_iris_columns_doesnt_contain_id_and_species():
    """
    GIVEN a new Iris dataset row
    WHEN the Iris model is created and `column_names` is called
    THEN the columns should not contain 'id' and 'species'
    """
    columns = Iris.column_names()
    assert 'species' not in columns
    assert 'id' not in columns


def test_csv_file_is_downloaded_and_inserted_into_db(init_database, csv_url):
    db = init_database
    FILENAME = csv_url.split("/")[-1]
    FetchCSV.download_csv_from_url(csv_url)
    assert os.path.exists(FILENAME) and os.path.isfile(FILENAME)
    assert db.session.query(db.func.count(Iris.id)).scalar() > 0
