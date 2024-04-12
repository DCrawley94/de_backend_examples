# Seeding with PG8000

An example repo for the seeding with PG8000 seminar.

## Setup

- Create a virtual environment
- Install [`pg8000`](https://pypi.org/project/pg8000/) into the virtual environment

To setup the example DB:

- `psql -f db/db-setup.sql`

This will create an database called named `nc_games`.

To seed the database set your `PYTHONPATH` and run this command: `python db/run-seed.py`

For querying the database you can use the `connect_to_db` function in the `db/connection.py` to create a connection object where it is needed.

## Included in the repo

**Solutions provided for a `GET` and `POST` endpoint**

![DB Schema](./db_schema.png)
