import json

from app.views import get_next_number


def test_sequence_elem_api_returns_valid_status(
    test_client, positive_non_zero_number_upto_thousand
):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/sequence/elem/' api is requested (GET)
         with positive number up to thousand
    THEN check that the response status is 200
    """
    response = test_client.get(
        f"/sequence/elem/{positive_non_zero_number_upto_thousand}/")
    assert response.status_code == 200


def test_sequence_elem_api_contains_limit(test_client, positive_non_zero_number_upto_thousand):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/sequence/elem/' api is requested (GET)
         with positive number up to thousand
    THEN check that the response contains 'limit'
    """
    response = test_client.get(
        f"/sequence/elem/{positive_non_zero_number_upto_thousand}/")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "limit" in data


def test_sequence_elem_api_contains_next_link_when_paginated(
    test_client, positive_non_zero_number_upto_thousand
):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/sequence/elem/' api is requested (GET)
         with positive number up to thousand and
         the response is paginated
    THEN check that the response contains 'next'
    """
    response = test_client.get(
        f"/sequence/elem/{positive_non_zero_number_upto_thousand}/?limit=1"
    )
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "next" in data


def test_sequence_elem_api_contains_all_elements_with_all_query_param(
    test_client, positive_non_zero_number_upto_thousand
):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/sequence/elem/' api is requested (GET)
         with positive number up to thousand
         and 'all' as a query param
    THEN check that the response contains all the
         elements of the sequence
    """
    response = test_client.get(
        f"/sequence/elem/{positive_non_zero_number_upto_thousand}/?all")
    data = json.loads(response.data)
    assert response.status_code == 200

    old = data["data"][0]
    for i in range(1, len(data["data"])):
        current = data["data"][i]
        assert current == get_next_number(old)
        old = current


def test_sequence_elem_api_doesnt_contain_limit_with_all_query_param(
    test_client, positive_non_zero_number_upto_thousand
):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/sequence/elem/' api is requested (GET)
         with positive number up to thousand
         and 'all' as a query param
    THEN check that the response doesn't contain limit
    """
    response = test_client.get(
        f"/sequence/elem/{positive_non_zero_number_upto_thousand}/?all")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["limit"] is None


def test_sequence_elem_api_doesnt_contain_next_with_all_query_param(
    test_client, positive_non_zero_number_upto_thousand
):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/sequence/elem/' api is requested (GET)
         with positive number up to thousand
         and 'all' as a query param
    THEN check that the response doesn't contain limit
    """
    response = test_client.get(
        f"/sequence/elem/{positive_non_zero_number_upto_thousand}/?all")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "next" not in data


def test_sequence_elem_api_error_with_invalid_number(test_client, invalid_number):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/sequence/elem/' api is requested (GET)
         with invalid number
    THEN check that the response status is 404
    """
    response = test_client.get(f"/sequence/elem/{invalid_number}/")
    assert response.status_code == 404


def test_sequence_longest_api_returns_valid_status(
    test_client, positive_non_zero_number_upto_thousand
):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/sequence/longest/' api is requested (GET)
         with positive number up to thousand
    THEN check that the response status is 200
    """
    response = test_client.get(
        f"/sequence/longest/{positive_non_zero_number_upto_thousand}/")
    assert response.status_code == 200


def test_sequence_longest_api_error_with_invalid_number(test_client, invalid_number):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/sequence/longest/' api is requested (GET)
         with invalid number
    THEN check that the response status is 404
    """
    response = test_client.get(f"/sequence/longest/{invalid_number}/")
    assert response.status_code == 404


def test_sequence_longest_api_returns_maximum_pair(test_client, number_with_maximum_pair):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/sequence/longest/' api is requested (GET)
         with a number
    THEN check that the response contain the number with maximum sequence length
    """
    number, maximum_pair = number_with_maximum_pair
    response = test_client.get(f"/sequence/longest/{number}/")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert maximum_pair[0] == data["data"]["longest"]
    assert maximum_pair[1] == data["data"]["number"]
