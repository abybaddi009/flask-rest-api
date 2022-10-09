import json
from collections import defaultdict
from functools import lru_cache

import pandas as pd
from flask import request, url_for
from flask_restful import Resource

from .database import db
from .models import Iris


def next_value_key(x): return f"element-{x}"
def length_key(x): return f"length-{x}"


@lru_cache(maxsize=1000)
def get_next_number(current):
    """
    Returns the next number in the sequence
    """
    if current < 1:
        return NotImplemented
    if current == 1:
        return 1
    return current // 2 if current % 2 == 0 else 3 * current + 1


@lru_cache(maxsize=1000)
def get_sequence_length(number):
    if number < 1:
        return NotImplemented
    if number == 1:
        return 1
    return get_sequence_length(get_next_number(number)) + 1


def naive_length_calculation(number):
    if number < 1:
        return 0

    length = 1
    while number != 1:
        number = 3 * number + 1 if number % 2 else number // 2
        length += 1
    return length


class SequenceElements(Resource):
    def get(self, n):
        response = defaultdict()

        try:
            limit = int(request.args.get("limit", 100))
        except ValueError:
            response["error"] = "`limit` should be a number"

        all_values = False if "all" not in request.args else True
        if all_values:
            limit = None
            response["all"] = True
        response["limit"] = limit

        if n < 1:
            # since the resource mapping to URL will only enable positive integers
            pass
        elif n == 1:
            response["data"] = [1]
        else:
            numbers = [
                n,
            ]
            while (n > 1 and not limit) or (n > 1 and len(numbers) < limit):
                n = get_next_number(n)
                numbers.append(n)
            response["data"] = numbers
            if n != 1:
                response["next"] = url_for(
                    "elem", n=get_next_number(n), limit=limit, all=all_values
                )

        return response, (200 if not "error" in response else 400)


class LongestSequence(Resource):
    def get(self, n):
        response = defaultdict()
        if n < 1:
            # since the resource mapping to URL will only enable positive integers
            pass
        elif n == 1:
            response["data"] = dict(longest=1, number=1)
        else:
            maximum = 1
            number = 1
            for i in range(1, n):
                current_size = get_sequence_length(i)
                if current_size > maximum:
                    maximum = current_size
                    number = i
            response["data"] = dict(longest=maximum, number=number)
        return response, (200 if not "error" in response else 400)


class CSVDescribe(Resource):
    """
    Returns basic statistics of the dataset
    """

    def get(self):
        response = defaultdict()
        query = db.session.query(Iris)
        df = pd.read_sql(query.statement, query.session.connection())
        response["data"] = json.loads(df.describe().to_json())
        return response, 200


class CSVGroup(Resource):
    """
    Computes species wise count based on the selected `column_name` having value upto the given `maximum value`

    Arguments:
        column_name: Column name from the Iris table
        maximum: Numeric value
    Returns list of {species: count}
    """

    def get(self, column_name, maximum):
        response = defaultdict()
        status = 200

        column_names = Iris.column_names()
        if column_name not in column_names:
            response[
                "error"
            ] = f"Invalid column name `{column_name}`. Possible values: {column_names}"
            status = 400
        else:
            try:
                maximum = float(maximum)
            except ValueError:
                response["error"] = "Value must be numeric"
                status = 400
            else:
                results = (
                    db.session.query(Iris.species, db.func.count(Iris.id))
                    .group_by(Iris.species)
                    .where(getattr(Iris, column_name) < maximum)
                )
                response["data"] = {}
                for row in results:
                    response["data"].update({row[0]: row[1]})
        return response, status
