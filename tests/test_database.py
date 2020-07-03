from app.database import fetchers, frontier, database, db_models, pyd_models
from app.common import common_values as c
from tests import rest_api as rest
from tests import db_query
from time import sleep

from sqlalchemy.sql.elements import BooleanClauseList

db = database.SessionLocal()


def test_get_fetcher_hashes():
    fetcher_amount = 10
    rest.delete_full_database(full=True)
    rest.create_database(fetcher_amount=fetcher_amount)

    fetcher_hashes = database.get_fetcher_hashes(db)
    print(fetcher_hashes)
    assert len(fetcher_hashes) == fetcher_amount * c.ch_hash_amount


def test_get_fetcher_hash_ranges():

    fetcher_amount = 5
    rest.delete_full_database(full=True)
    rest.create_database(fetcher_amount=fetcher_amount)

    uuid = db_query.get_fetcher_uuid_with_max_hash(db)
    fetcher_hash_range = database.get_fetcher_hash_ranges(db, uuid)

    print(fetcher_hash_range)
    assert len(fetcher_hash_range) == c.ch_hash_amount
    assert fetcher_hash_range[-1][-1] == db_query.get_min_hash(db)
    assert fetcher_hash_range[0][1] < fetcher_hash_range[0][2]
    assert fetcher_hash_range[-1][1] > fetcher_hash_range[0][1]


def test_hash_range_query_filter():
    fetcher_hash_range = [("id1", 2, 3), ("id2", 4, 5), ("id3", 7, 1)]

    filter_query = database.get_hash_range_filter_query(fetcher_hash_range)
    print(filter_query)

    assert isinstance(filter_query, BooleanClauseList)


def test_bigger_hash_range_query_filter():
    hash_range = [
        (
            "cf1cd50f-9b4e-4392-adaf-b2ef524018d1",
            636080131184570666,
            644892773925397330,
        ),
        (
            "cf1cd50f-9b4e-4392-adaf-b2ef524018d1",
            1396368064292172472,
            1527370026380014933,
        ),
        (
            "cf1cd50f-9b4e-4392-adaf-b2ef524018d1",
            7027753529162109501,
            7069658322666814073,
        ),
        (
            "cf1cd50f-9b4e-4392-adaf-b2ef524018d1",
            9135798451549758696,
            85190412353678244,
        ),
    ]

    filter_query = database.get_hash_range_filter_query(hash_range)
    print(filter_query)

    assert isinstance(filter_query, BooleanClauseList)
    assert len(filter_query) == len(hash_range)