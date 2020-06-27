from fastapi.testclient import TestClient

from app.main import app
from app.database import frontier, pyd_models, database
from app.common import random_data_generator as rand_gen, common_values as c

client = TestClient(app)
db = database.SessionLocal()


# Database
def delete_full_database_with_rest(
    full=False,
    url_refs=False,
    fetchers=False,
    urls=False,
    fqdns=False,
    reserved_fqdns=False,
):
    if full:
        url_refs = True
        fetchers = True
        urls = True
        fqdns = True
        reserved_fqdns = True
    client.delete(
        c.database_endpoint,
        json={
            "delete_url_refs": url_refs,
            "delete_fetchers": fetchers,
            "delete_urls": urls,
            "delete_fqdns": fqdns,
            "delete_reserved_fqdns": reserved_fqdns,
        },
    )


def create_database_with_rest(
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


def get_first_crawler_uuid_with_rest():
    return client.get(c.fetcher_endpoint).json()[0]["uuid"]


def get_simple_frontier_with_rest(uuid):
    return client.post(
        c.frontier_endpoint,
        json={"fetcher_uuid": uuid, "amount": 2, "length": 10, "tld": "de"},
    ).json()


def get_frontier_with_rest(json_dict):
    return client.post(c.frontier_endpoint, json=json_dict,).json()


def get_stats_with_rest():
    return client.get(c.stats_endpoint).json()


def get_random_urls_with_rest(amount: int = 1):
    return client.get("/urls/", json={"amount": amount}).json()


def activate_fqdn_hash():
    client.patch("/settings/", json={"long_term_part_mode": "fqdn_hash"})


def deactivate_fqdn_hash():
    client.patch("/settings/", json={"long_term_part_mode": "none"})
