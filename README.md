# Flask based Rest API application

- [Flask based Rest API application](#flask-based-rest-api-application)
  - [Assumptions](#assumptions)
    - [Part 1: Sequence](#part-1-sequence)
    - [Part 2: Iris & pandas](#part-2-iris--pandas)
  - [Running the code](#running-the-code)
    - [Pre-requisites](#pre-requisites)
    - [Install dependencies](#install-dependencies)
    - [Running the server](#running-the-server)
  - [Testing the code](#testing-the-code)

Flask based Rest API with:
* pytest for testing
* SQLAlchemy as ORM layer
* Redis for caching
* gunicorn as web server

## Assumptions

### Part 1: Sequence

1. To facilitate faster retrieval, sub problems are cached with an in-built function.
2. To enable computation of long sequences, /sequence/elem/ is paginated with `limit` query param.
3. To fetch all the elements of a sequence `all` can be supplied as a query param.

### Part 2: Iris & pandas

1. To enable retrieval of large dataset, the `CSV_URL` is streamed
2. For automatic update to the local dataset, the `download_csv_from_url` fetches and appends to the disk when the URL has more rows. And it only inserts rows that are not added to the table.

## Running the code

### Pre-requisites

* Python 3.7+

### Install dependencies

1. Create a virtual environment
    
        python -m venv .env


2. Install all the dependencies from requirements.txt

        pip install -r requirements.txt

### Running the server

1. Check the configuration in the config.py
2. Run `./start_server.sh` for *nix based OS and `start_server` for Windows

## Testing the code

Test suite has been added for pytest. Run with: 

    pytest -v
