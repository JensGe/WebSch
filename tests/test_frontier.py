from fastapi.testclient import TestClient

from app.main import app
from app.database import frontier, pyd_models, database
from app.common import random_data_generator as rand_gen, common_values as c

from tests import values as v
from time import sleep

from pydantic import HttpUrl

example_domain_com = "www.example.com"
example_domain_de = "www.example.com"


client = TestClient(app)
db = database.SessionLocal()


def test_get_url_from_frontier_response():
    frontier_one = pyd_models.UrlFrontier(
        fqdn=example_domain_com,
        tld="com",
        url_list=[
            pyd_models.Url(
                url=HttpUrl(
                    url="http://www.example.com/abcefg", scheme="http", host="example"
                ),
                fqdn=example_domain_com,
            ),
            pyd_models.Url(
                url=HttpUrl(
                    url="http://www.example.com/hijklm", scheme="http", host="example"
                ),
                fqdn=example_domain_com,
            ),
        ],
    )

    frontier_two = pyd_models.UrlFrontier(
        fqdn=example_domain_de,
        tld="de",
        url_list=[
            pyd_models.Url(
                url=HttpUrl(
                    url="http://www.example.de/abcefg", scheme="http", host="example"
                ),
                fqdn=example_domain_de,
            ),
            pyd_models.Url(
                url=HttpUrl(
                    url="http://www.example.de/hijklm", scheme="http", host="example"
                ),
                fqdn=example_domain_de,
            ),
        ],
    )

    frontier_response = pyd_models.FrontierResponse(
        uuid=v.sample_uuid,
        response_url="http://www.example.com/submit?code=1234567890",
        withdrawal_date=rand_gen.get_random_datetime(),
        url_frontiers=[frontier_one, frontier_two],
    )
    frontier_response.url_frontiers_count = len(frontier_response.url_frontiers)

    urls_count = 0
    for url_frontier in frontier_response.url_frontiers:
        urls_count += len(url_frontier.url_list)

    frontier_response.urls_count = urls_count

    url_list = frontier.get_url_list_from_frontier_response(frontier_response)

    assert frontier_response.url_frontiers_count == 2
    assert frontier_response.urls_count == 4
    assert url_list == [
        HttpUrl(url="http://www.example.com/abcefg", scheme="http", host="example"),
        HttpUrl(url="http://www.example.com/hijklm", scheme="http", host="example"),
        HttpUrl(url="http://www.example.de/abcefg", scheme="http", host="example"),
        HttpUrl(url="http://www.example.de/hijklm", scheme="http", host="example"),
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
            "crawler_amount": 0,
            "fqdn_amount": 5,
            "min_url_amount": 2,
            "max_url_amount": 2,
            "connection_amount": 0,
        },
    )
    sleep(10)

    frontier_request = pyd_models.FrontierRequest(
        crawler_uuid=v.sample_uuid, amount=2, length=2
    )

    fqdn_list = frontier.get_fqdn_list(db, frontier_request)
    print(fqdn_list)
    assert len(fqdn_list) == 2
