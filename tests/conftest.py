import os
import random

import pytest

from app import create_app, db
from app.dataset import FetchCSV
from app.models import Iris
from app.views import naive_length_calculation


@pytest.fixture(scope="module")
def flask_app():
    return create_app()


@pytest.fixture(scope="module")
def test_client(flask_app):

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client


@pytest.fixture(scope="module")
def init_database(test_client):
    # Create the database and the database table
    db.create_all()

    # in case the file already exists, take a backup
    if os.path.exists("iris.csv"):
        os.rename("iris.csv", "iris.bak")

    yield db

    # restore the file
    if os.path.exists("iris.bak"):
        os.rename("iris.bak", "iris.csv")

    db.drop_all()


@pytest.fixture(scope="function")
def csv_url():
    return "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"


@pytest.fixture(scope="function")
def download_csv(flask_app, init_database, csv_url):
    FetchCSV.download_csv_from_url(csv_url)
    return


@pytest.fixture(scope="function")
def new_irisrow():
    iris = Iris(
        sepal_length=random.random() * 10,
        sepal_width=random.random() * 10,
        petal_length=random.random() * 10,
        petal_width=random.random() * 10,
        species="random",
    )
    return iris


@pytest.fixture(scope="function")
def positive_even_number():
    return random.randint(1, 10**10) * 2


@pytest.fixture(scope="function")
def positive_odd_number():
    return random.randint(1, 10**10) * 2 - 1


@pytest.fixture(scope="function")
def negative_number():
    return -random.randint(1, 10**10)


@pytest.fixture(scope="function")
def positive_non_zero_number_upto_ten():
    return random.randint(1, 10)


@pytest.fixture(scope="function")
def positive_non_zero_number_upto_thousand():
    return random.randint(1, 10**3)


@pytest.fixture(scope="function")
def invalid_number():
    return "foo"


@pytest.fixture(scope="function")
def number_with_maximum_pair():
    number = random.randint(2, 10)
    maximum_pair = max([(naive_length_calculation(i), i)
                       for i in range(1, number)])
    return number, maximum_pair
