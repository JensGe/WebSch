from app.database import frontier, db_models, pyd_models
from app.common import random_data_generator as rand_gen
from tests import values as v
from pydantic import HttpUrl

example_domain_com = "www.example.com"
example_domain_de = "www.example.com"


def test_get_url_from_frontier_response():
    single_frontier_one = pyd_models.UrlFrontier(
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

    single_frontier_two = pyd_models.UrlFrontier(
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
        url_frontiers_count=2,
        urls_count=2,
        url_frontiers=[single_frontier_one, single_frontier_two],
    )

    url_list = frontier.get_url_list_from_frontier_response(frontier_response)

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

