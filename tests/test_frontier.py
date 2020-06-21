from fastapi.testclient import TestClient

from app.main import app
from app.database import frontier, pyd_models, database
from app.common import random_data_generator as rand_gen, common_values as c

from app.database import db_models

from tests import values as v
from time import sleep
from datetime import datetime, timedelta, timezone

from pydantic import HttpUrl

example_domain_com = "www.example.com"
example_domain_de = "www.example.com"


client = TestClient(app)
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


def test_get_fqdn_list():
    client.post(
        c.database_endpoint,
        json={
            "fetcher_amount": 0,
            "fqdn_amount": 5,
            "min_url_amount": 2,
            "max_url_amount": 2,
            "connection_amount": 0,
        },
    )
    sleep(3)

    frontier_request = pyd_models.FrontierRequest(
        fetcher_uuid=v.sample_uuid, amount=2, length=2
    )

    fqdn_list = frontier.create_fqdn_list(db, frontier_request)
    assert len(fqdn_list) == 2


def test_save_reservations_with_old_entries():
    client.post(
        c.database_endpoint,
        json={
            "fetcher_amount": 1,
            "fqdn_amount": 5,
            "min_url_amount": 2,
            "max_url_amount": 2,
            "connection_amount": 0,
        },
    )
    sleep(3)

    fetcher_uuid = client.get(c.fetcher_endpoint).json()[0]["uuid"]

    response = client.post(
        c.frontier_endpoint,
        json={"fetcher_uuid": fetcher_uuid, "amount": 2, "length": 10, "tld": "de"},
    ).json()

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
    client.post(
        c.database_endpoint,
        json={
            "fetcher_amount": 0,
            "fqdn_amount": 1,
            "min_url_amount": 1,
            "max_url_amount": 1,
            "visited_ratio": 0.0,
            "connection_amount": 0,
        },
    )

    sleep(3)

    stats_before = client.get(c.stats_endpoint).json()

    client.post(
        c.database_endpoint,
        json={
            "fetcher_amount": 0,
            "fqdn_amount": 1,
            "min_url_amount": 1,
            "max_url_amount": 1,
            "visited_ratio": 0.0,
            "connection_amount": 1,
        },
    )

    sleep(3)

    stats_after = client.get(c.stats_endpoint).json()
    assert stats_after["url_amount"] == stats_before["url_amount"] + 1
    assert stats_after["url_ref_amount"] == stats_before["url_ref_amount"] + 1


def test_get_random_urls():
    client.post(
        c.database_endpoint,
        json={
            "fetcher_amount": 0,
            "fqdn_amount": 1,
            "min_url_amount": 10,
            "max_url_amount": 10,
            "connection_amount": 0,
        },
    )
    sleep(3)

    result = client.get("/urls/", json={"amount": 5}).json()
    print(result)
    assert len(result["url_list"]) == 5


def test_query_avg_freshness():
    avg_fresh = frontier.calculate_avg_freshness(db)
    assert isinstance(avg_fresh, str)


def test_set_fetcher_settings():
    request = pyd_models.FetcherSettings(iterations=1)
    rv = frontier.set_fetcher_settings(request, db)

    assert rv.iterations == request.iterations
