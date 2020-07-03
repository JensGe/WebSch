from app.database import frontier, pyd_models, database
from app.common import random_data_generator as rand_gen, common_values as c, enum

from app.database import db_models

from tests import values as v
from tests import rest_api as rest
from tests import db_query
from time import sleep
from datetime import datetime, timedelta, timezone

from pydantic import HttpUrl

example_domain_com = "www.example.com"
example_domain_de = "www.example.com"

db = database.SessionLocal()


def create_example_frontier_response(uuid=v.sample_uuid):
    frontier_one = pyd_models.Frontier(
        fqdn=example_domain_com,
        tld="com",
        url_list=[
            pyd_models.Url(
                url=HttpUrl(
                    url="https://www.example.com/abcefg", scheme="http", host="example"
                ),
                fqdn=example_domain_com,
            ),
            pyd_models.Url(
                url=HttpUrl(
                    url="https://www.example.com/hijklm", scheme="http", host="example"
                ),
                fqdn=example_domain_com,
            ),
        ],
    )

    frontier_two = pyd_models.Frontier(
        fqdn=example_domain_de,
        tld="de",
        url_list=[
            pyd_models.Url(
                url=HttpUrl(
                    url="https://www.example.de/abcefg", scheme="http", host="example"
                ),
                fqdn=example_domain_de,
            ),
            pyd_models.Url(
                url=HttpUrl(
                    url="https://www.example.de/hijklm", scheme="http", host="example"
                ),
                fqdn=example_domain_de,
            ),
        ],
    )

    frontier_response = pyd_models.FrontierResponse(
        uuid=uuid,
        response_url="https://www.example.com/submit?code=1234567890",
        latest_return=rand_gen.random_datetime(),
        url_frontiers=[frontier_one, frontier_two],
    )
    frontier_response.url_frontiers_count = len(frontier_response.url_frontiers)

    urls_count = 0
    for url_frontier in frontier_response.url_frontiers:
        urls_count += len(url_frontier.url_list)

    frontier_response.urls_count = urls_count

    return frontier_response


def test_get_url_from_frontier_response():

    frontier_response = create_example_frontier_response()

    url_list = frontier.get_url_list_from_frontier_response(frontier_response)

    assert frontier_response.url_frontiers_count == 2
    assert frontier_response.urls_count == 4
    assert url_list == [
        HttpUrl(url="https://www.example.com/abcefg", scheme="http", host="example"),
        HttpUrl(url="https://www.example.com/hijklm", scheme="http", host="example"),
        HttpUrl(url="https://www.example.de/abcefg", scheme="http", host="example"),
        HttpUrl(url="https://www.example.de/hijklm", scheme="http", host="example"),
    ]


def test_difference_two_string_lists():
    old_list = ["abc", "def", "ghi"]
    new_list = ["def", "jkl", "ghi"]
    asserted_only_in_new_list = ["jkl"]

    only_in_new_list = frontier.get_only_new_list_items(new_list, old_list)

    assert only_in_new_list == asserted_only_in_new_list


def test_create_fqdn_list():
    rest.delete_full_database(full=True)
    rest.create_database(fetcher_amount=3, fqdn_amount=10)
    uuid = rest.get_first_fetcher_uuid()

    frontier_request = pyd_models.FrontierRequest(fetcher_uuid=uuid, amount=2, length=2)

    fqdn_list = frontier.create_fqdn_list(db, frontier_request)
    assert len(fqdn_list) == 2


def test_save_reservations_with_old_entries():
    rest.delete_full_database(full=True)
    rest.create_database(fetcher_amount=3, fqdn_amount=10)

    fetcher_uuid = rest.get_first_fetcher_uuid()

    response = rest.get_simple_frontier(fetcher_uuid)

    fqdn = response["url_frontiers"][0]["fqdn"]

    frontier_response = pyd_models.FrontierResponse(
        uuid=fetcher_uuid,
        response_url=response["response_url"],
        latest_return=response["latest_return"],
        url_frontiers_count=response["url_frontiers_count"],
        urls_count=response["urls_count"],
        url_frontiers=response["url_frontiers"],
    )

    reservation_item = (
        db.query(db_models.FetcherReservation)
        .filter(db_models.FetcherReservation.fetcher_uuid == fetcher_uuid)
        .filter(db_models.FetcherReservation.fqdn == fqdn)
        .first()
    )
    reservation_item.latest_return = datetime.now(tz=timezone.utc) - timedelta(days=2)
    db.commit()
    db.refresh(reservation_item)

    assert frontier.save_reservations(
        db, frontier_response, datetime.now(tz=timezone.utc)
    )


def test_get_referencing_urls():
    rest.delete_full_database(full=True)
    rest.create_database()

    sleep(1)
    stats_before = rest.get_stats()

    rest.create_database(connection_amount=1)

    stats_after = rest.get_stats()

    assert stats_after["url_amount"] == stats_before["url_amount"] + 1
    assert stats_after["url_ref_amount"] == stats_before["url_ref_amount"] + 1


def test_get_random_urls():
    rest.delete_full_database(full=True)
    rest.create_database(min_url_amount=10, max_url_amount=10)

    result = rest.get_random_urls(amount=5)

    assert len(result["url_list"]) == 5


def test_query_avg_freshness():
    avg_fresh = frontier.calculate_avg_freshness(db)
    assert isinstance(avg_fresh, str)


def test_query_fqdn_hash_range():
    rest.delete_full_database(full=True)
    rest.create_database(fetcher_amount=3, fqdn_amount=50)

    result = frontier.get_fqdn_hash_range(db)
    assert isinstance(result, float)


def test_set_fetcher_settings():
    request = pyd_models.FetcherSettings(iterations=1)
    rv = frontier.set_fetcher_settings(request, db)

    assert rv.iterations == request.iterations


def test_fqdn_hash_activated():
    rest.activate_fqdn_hash()
    assert database.fqdn_hash_activated(db) is True


def test_fqdn_hash_deactivated():
    rest.reset_long_term_part_strategy()
    assert database.fqdn_hash_activated(db) is False


def test_consistent_hash_activated():
    rest.activate_consistent_hash()
    assert database.consistent_hash_activated(db) is True


def test_consistent_hash_deactivated():
    rest.reset_long_term_part_strategy()
    assert database.fqdn_hash_activated(db) is False


# def test_get_hash_range_with_db():
#     rest.delete_full_database(full=True)
#     rest.create_database(fetcher_amount=5)
#
#     uuid = rest.get_first_fetcher_uuid()
#     fetcher_hashes = (
#         db.query(db_models.Fetcher.uuid, db_models.Fetcher.fetcher_hash)
#         .order_by(db_models.Fetcher.fetcher_hash.asc())
#         .all()
#     )
#
#     print(fetcher_hashes)
#
#     min_hash, max_hash = frontier.get_hash_range(fetcher_hashes, uuid)
#     print("min: {}, max: {}".format(min_hash, max_hash))
#     assert isinstance(min_hash, int)
#     assert isinstance(max_hash, int)
#     assert min_hash < max_hash or max_hash == fetcher_hashes[0][1]

#
# def test_get_hash_pure():
#     uuid = "9b200069-3773-4270-aa1c-2d89c1335623"
#     fetcher_hashes = [
#         ("9b200069-3773-4270-aa1c-2d89c1335623", 2537359433),
#         ("2ac1e563-5261-4044-9f94-36a09726d00f", 2638481537),
#         ("cd21a2f3-c808-453f-b2ee-3e45e01a7573", 2999322988),
#     ]
#
#     min_hash, max_hash = frontier.get_hash_range(fetcher_hashes, uuid)
#     assert min_hash == fetcher_hashes[0][1]
#     assert max_hash == fetcher_hashes[1][1]
#
#
# def test_get_hash_pure_circled():
#     uuid = "cd21a2f3-c808-453f-b2ee-3e45e01a7573"
#     fetcher_hashes = [
#         ("9b200069-3773-4270-aa1c-2d89c1335623", 2537359433),
#         ("2ac1e563-5261-4044-9f94-36a09726d00f", 2638481537),
#         ("cd21a2f3-c808-453f-b2ee-3e45e01a7573", 2999322988),
#     ]
#
#     min_hash, max_hash = frontier.get_hash_range(fetcher_hashes, uuid)
#     assert min_hash == fetcher_hashes[2][1]
#     assert max_hash == fetcher_hashes[0][1]


def test_create_fqdn_list_with_consistent_hashing():
    rest.delete_full_database(full=True)
    rest.create_database(fetcher_amount=3, fqdn_amount=100)

    uuid = db_query.get_fetcher_uuid_with_max_hash(db)
    request = pyd_models.FrontierRequest(
        fetcher_uuid=uuid,
        amount=0,
        long_term_part_mode=enum.LONGPART.consistent_hashing,
    )
    fqdn_list = frontier.create_fqdn_list(db, request)

    print(fqdn_list)

    assert len(fqdn_list) > 5
    assert len(fqdn_list) < 60
