import json
import os

import pandas as pd

from app.dataset import FetchCSV
from app.models import Iris


def test_iris_describe_api_returns_valid_status(
    test_client
):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/iris/describe/' api is requested (GET)
    THEN check that the response status is 200
    """
    response = test_client.get(f"/iris/describe/")
    assert response.status_code == 200


def test_iris_describe_api_returns_correct_description(
    test_client, download_csv, csv_url
):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/iris/describe/' api is requested (GET)
    THEN check that the response contains valid description
    """
    response = test_client.get(f"/iris/describe/")
    assert response.status_code == 200
    df = pd.read_csv(csv_url.split("/")[-1])
    data = json.loads(df.describe().to_json())
    response_data = json.loads(response.data)["data"]
    for key, value in data.items():
        assert key in response_data
        assert value == response_data[key]


def test_iris_sepal_length_api_returns_valid_status(
    test_client, positive_non_zero_number_upto_ten
):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/iris/sepal_length/' api is requested (GET)
    THEN check that the response status is 200
    """
    response = test_client.get(
        f"/iris/sepal_length/{positive_non_zero_number_upto_ten}/")
    assert response.status_code == 200


def test_iris_sepal_width_api_returns_valid_status(
    test_client, positive_non_zero_number_upto_ten
):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/iris/sepal_width/' api is requested (GET)
    THEN check that the response status is 200
    """
    response = test_client.get(
        f"/iris/sepal_width/{positive_non_zero_number_upto_ten}/")
    assert response.status_code == 200


def test_iris_petal_length_api_returns_valid_status(
    test_client, positive_non_zero_number_upto_ten
):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/iris/petal_length/' api is requested (GET)
    THEN check that the response status is 200
    """
    response = test_client.get(
        f"/iris/petal_length/{positive_non_zero_number_upto_ten}/")
    assert response.status_code == 200


def test_iris_petal_width_api_returns_valid_status(
    test_client, positive_non_zero_number_upto_ten
):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/iris/petal_width/' api is requested (GET)
    THEN check that the response status is 200
    """
    response = test_client.get(
        f"/iris/petal_width/{positive_non_zero_number_upto_ten}/")
    assert response.status_code == 200


def test_iris_group_api_error_with_invalid_column(
    test_client, positive_non_zero_number_upto_ten
):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/iris/petal_width/' api is requested (GET)
    THEN check that the response status 400
    """
    response = test_client.get(
        f"/iris/foo/{positive_non_zero_number_upto_ten}/")
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["error"] != ""


def test_iris_group_api_error_with_invalid_number(
    test_client, invalid_number
):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/iris/petal_width/' api is requested (GET)
    THEN check that the response status 400
    """
    response = test_client.get(f"/iris/sepal_width/{invalid_number}/")
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["error"] != ""


def test_iris_sepal_length_maximum_count(test_client, download_csv, csv_url):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/iris/sepal_length/' api is requested with maximum of 5
    THEN check that the response contains correct species count
    """
    maximum = 5
    response = test_client.get(f"/iris/sepal_length/{maximum}/")
    assert response.status_code == 200
    df = pd.read_csv(csv_url.split("/")[-1])
    new_df = df[["sepal_length", "species"]]
    df_data = new_df[new_df["sepal_length"] < 5].groupby(
        "species").count().to_dict()
    response_data = json.loads(response.data)["data"]
    for species, count in response_data.items():
        assert df_data["sepal_length"][species] == count
