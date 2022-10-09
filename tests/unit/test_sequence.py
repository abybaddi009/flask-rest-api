from app.views import (get_next_number, get_sequence_length,
                       naive_length_calculation)


def test_sequence_next_number_even(positive_even_number):
    """
    GIVEN a positive even starting number
    WHEN `get_next_number` is called
    THEN the returned number should be divided by two
    """
    assert get_next_number(positive_even_number) == positive_even_number // 2


def test_sequence_next_number_odd(positive_odd_number):
    """
    GIVEN a positive odd starting number
    WHEN `get_next_number` is called
    THEN the returned number should be divided by two
    """
    assert get_next_number(positive_odd_number) == 3 * positive_odd_number + 1


def test_sequence_next_number_for_one():
    """
    GIVEN the number one as input
    WHEN `get_next_number` is called
    THEN the returned number should be one
    """
    assert get_next_number(1) == 1


def test_sequence_next_number_for_zero():
    """
    GIVEN the number zero as input
    WHEN `get_next_number` is called
    THEN the returned value should be `NotImplemented`
    """
    assert get_next_number(0) == NotImplemented


def test_sequence_next_number_for_negative_number(negative_number):
    """
    GIVEN a negative number as input
    WHEN `get_next_number` is called
    THEN the returned value should be `NotImplemented`
    """
    assert get_next_number(negative_number) == NotImplemented


def test_sequence_length_for_one():
    """
    GIVEN the number one as input
    WHEN `get_sequence_length` is called
    THEN the returned number should be one
    """
    assert get_sequence_length(1) == 1


def test_sequence_length_for_positive_number(positive_non_zero_number_upto_thousand):
    """
    GIVEN a positive number up to thousand as input
    WHEN `get_sequence_length` is called
    THEN the returned number should match the `naive_length_calculation`
    """
    assert get_sequence_length(positive_non_zero_number_upto_thousand) == naive_length_calculation(
        positive_non_zero_number_upto_thousand)
