from fastapi.testclient import TestClient

from app.main import app
from app.database import database
from app.common import enum
from app.common import common_values as c

client = TestClient(app)
db = database.SessionLocal()


# Database
def delete_full_database(
    full=False,
    url_refs=False,
    fetcher_hashes=False,
    fetchers=False,
    urls=False,
    fqdns=False,
    reserved_fqdns=False,
):
    if full:
        url_refs = True
        fetcher_hashes = True
        fetchers = True
        urls = True
        fqdns = True
        reserved_fqdns = True
    client.delete(
        c.database_endpoint,
        json={
            "delete_url_refs": url_refs,
            "delete_fetcher_hashes": fetcher_hashes,
            "delete_fetchers": fetchers,
            "delete_urls": urls,
            "delete_fqdns": fqdns,
            "delete_reserved_fqdns": reserved_fqdns,
        },
    )


def create_database(
    fetcher_amount: int = 1,
    fqdn_amount: int = 1,
    min_url_amount: int = 1,
    max_url_amount: int = 1,
    visited_ratio: float = 0.0,
    connection_amount: int = 0,
):
    client.post(
        c.database_endpoint,
        json={
            "fetcher_amount": fetcher_amount,
            "fqdn_amount": fqdn_amount,
            "min_url_amount": min_url_amount,
            "max_url_amount": max_url_amount,
            "visited_ratio": visited_ratio,
            "connection_amount": connection_amount,
        },
    )


def get_first_fetcher_uuid():
    return client.get(c.fetcher_endpoint).json()[0]["uuid"]


def get_fetcher_uuids():
    fetcher_obj = client.get(c.fetcher_endpoint).json()
    return [fetcher["uuid"] for fetcher in fetcher_obj]


def get_simple_frontier(uuid):
    return client.post(
        c.frontier_endpoint,
        json={"fetcher_uuid": uuid, "amount": 2, "length": 10, "tld": "de"},
    ).json()


def get_frontier(json_dict):
    return client.post(c.frontier_endpoint, json=json_dict,).json()


def get_stats():
    return client.get(c.stats_endpoint).json()


def get_random_urls(amount: int = 1):
    return client.get(c.urls_endpoint, json={"amount": amount}).json()


def activate_fqdn_hash():
    client.put(
        c.settings_endpoint, json={"long_term_part_mode": enum.LONGPART.fqdn_hash}
    )


def activate_consistent_hash():
    client.put(
        c.settings_endpoint,
        json={"long_term_part_mode": enum.LONGPART.consistent_hashing},
    )


def reset_long_term_part_strategy():
    client.put(c.settings_endpoint, json={"long_term_part_mode": enum.LONGPART.none})
