from fastapi.testclient import TestClient
from fastapi import status

from app.main import app
from app.common import common_values as c, enum
from app.database import fetchers, frontier, database, db_models, pyd_models


from time import sleep
from tests import values as v
from tests import rest_api as rest

from sqlalchemy import or_, and_
from sqlalchemy.sql.expression import func
from collections import defaultdict

client = TestClient(app)
db = database.SessionLocal()


# Fetcher API
def test_get_all_fetcher():
    fetchers.delete_fetchers(db)
    client.post(c.fetcher_endpoint, json={"contact": v.test_email_1, "name": "IsaacV"})
    client.post(c.fetcher_endpoint, json={"contact": v.test_email_1, "name": "IsaacVI"})
    json_response = client.get(c.fetcher_endpoint).json()
    assert len(json_response) == 2


def test_create_fetcher():
    fetchers.delete_fetchers(db)
    response = client.post(
        c.fetcher_endpoint,
        json={
            "contact": "jens@honzont.de",
            "name": "IsaacIV",
            "location": "Germany",
            "tld_preference": "de",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_create_fetcher_duplicate():
    fetchers.delete_fetchers(db)
    client.post(c.fetcher_endpoint, json={"contact": v.test_email_1, "name": "IsaacIV"})
    response2 = client.post(
        c.fetcher_endpoint, json={"contact": v.test_email_1, "name": "IsaacIV"}
    )
    assert response2.status_code == status.HTTP_409_CONFLICT


def test_update_fetcher():
    fetchers.delete_fetchers(db)
    create_response = client.post(
        c.fetcher_endpoint,
        json={"contact": v.test_email_1, "name": "IsaacIV", "location": "Germany"},
    ).json()
    uuid = create_response["uuid"]
    contact = create_response["contact"]
    name = "IsaacXII"
    update_response = client.put(
        c.fetcher_endpoint, json={"uuid": uuid, "contact": contact, "name": name}
    )
    assert update_response.status_code == status.HTTP_200_OK
    assert update_response.json()["location"] is None


def test_update_unknown_fetcher():
    update_response = client.put(c.fetcher_endpoint, json={"uuid": v.sample_uuid},)
    assert update_response.status_code == status.HTTP_404_NOT_FOUND


def test_update_to_duplicate_fetcher():
    # ToDo
    assert True


def test_patch_fetcher_mix():
    fetchers.delete_fetchers(db)
    create_response = client.post(
        c.fetcher_endpoint,
        json={
            "contact": v.test_email_1,
            "name": "IsaacIV",
            "location": "Germany",
            "tld_preference": "de",
        },
    ).json()
    uuid = create_response["uuid"]
    name = "IsaacIX"

    update_response = client.patch(
        c.fetcher_endpoint, json={"uuid": uuid, "name": name}
    )
    assert update_response.status_code == status.HTTP_200_OK
    assert update_response.json()["name"] == "IsaacIX"
    assert update_response.json()["location"] == "Germany"


def test_patch_unknown_fetcher():
    patch_response = client.patch(c.fetcher_endpoint, json={"uuid": v.sample_uuid},)
    assert patch_response.status_code == status.HTTP_404_NOT_FOUND


def test_patch_fetcher_empty_patch():
    fetchers.delete_fetchers(db)
    create_response = client.post(
        c.fetcher_endpoint,
        json={
            "contact": v.test_email_1,
            "name": "IsaacIII",
            "location": "Germany",
            "tld_preference": "de",
        },
    ).json()

    uuid = create_response["uuid"]
    update_response = client.patch(c.fetcher_endpoint, json={"uuid": uuid})
    assert update_response.status_code == status.HTTP_200_OK
    assert update_response.json()["name"] == "IsaacIII"
    assert update_response.json()["location"] == "Germany"
    assert update_response.json()["tld_preference"] == "de"


def test_patch_fetcher_full_patch():
    fetchers.delete_fetchers(db)
    create_response = client.post(
        c.fetcher_endpoint,
        json={
            "contact": v.test_email_1,
            "name": "IsaacXXI",
            "location": "Germany",
            "tld_preference": "de",
        },
    ).json()

    uuid = create_response["uuid"]
    update_response = client.patch(
        c.fetcher_endpoint,
        json={
            "uuid": uuid,
            "name": "IsaacXXII",
            "location": "Sweden",
            "tld_preference": "se",
        },
    )
    assert update_response.status_code == status.HTTP_200_OK
    assert update_response.json()["name"] == "IsaacXXII"
    assert update_response.json()["location"] == "Sweden"
    assert update_response.json()["tld_preference"] == "se"


def test_patch_to_duplicate_fetcher():
    # ToDo
    assert True


def test_delete_fetcher():
    fetchers.delete_fetchers(db)
    json_response = client.post(
        c.fetcher_endpoint, json={"contact": v.test_email_1, "name": "IsaacVII"}
    ).json()
    created_uuid = json_response["uuid"]
    print("UUID: {}".format(created_uuid))
    delete_response = client.delete(c.fetcher_endpoint, json={"uuid": created_uuid})

    assert delete_response.status_code == status.HTTP_204_NO_CONTENT
    assert delete_response.content == b""

    json_response = client.get(c.fetcher_endpoint).json()
    assert len(json_response) == 0


def test_delete_unknown_fetcher():
    fetchers.delete_fetchers(db)
    delete_response = client.delete(c.fetcher_endpoint, json={"uuid": v.sample_uuid})

    assert delete_response.status_code == status.HTTP_404_NOT_FOUND


# Frontier API
def test_get_simple_frontier():
    client.delete(
        c.database_endpoint,
        json={
            "delete_reserved_fqdns": True,
            "delete_url_refs": True,
            "delete_fetchers": True,
            "delete_urls": True,
            "delete_fqdns": True,
        },
    )
    sleep(3)

    new_fetcher_uuid = client.post(
        c.fetcher_endpoint, json={"contact": v.test_email_1, "name": "Isaac"}
    ).json()["uuid"]

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
    sleep(5)

    response = client.post(
        c.frontier_endpoint,
        json={"fetcher_uuid": new_fetcher_uuid, "amount": 2, "length": 2},
    )
    print(response)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["url_frontiers_count"] == 2
    assert response.json()["urls_count"] == 4


def test_get_simple_frontier_with_bad_uuid():
    fetchers.delete_fetchers(db)
    response = client.post(
        c.frontier_endpoint,
        json={"fetcher_uuid": v.sample_uuid, "amount": 1, "length": 1},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_frontiers():
    fetchers.delete_fetchers(db)
    new_fetcher_uuid = client.post(
        c.fetcher_endpoint, json={"contact": v.test_email_1, "name": "Isaac"}
    ).json()["uuid"]

    response1 = client.post(
        c.frontier_endpoint,
        json={
            "fetcher_uuid": new_fetcher_uuid,
            "amount": 1,
            "length": 1,
            "prio_mode": enum.SHORTPRIO.old_pages_first,
        },
    )
    assert response1.status_code == status.HTTP_200_OK

    response2 = client.post(
        c.frontier_endpoint,
        json={
            "fetcher_uuid": new_fetcher_uuid,
            "amount": 1,
            "length": 1,
            "prio_mode": enum.SHORTPRIO.change_rate,
        },
    )
    assert response2.status_code == status.HTTP_200_OK


def test_get_fqdn_list_with_fqdn_hash():
    rest.delete_full_database(full=True)
    rest.create_database(fetcher_amount=3, fqdn_amount=50)

    fetcher_uuid = rest.get_first_fetcher_uuid()

    response = rest.get_frontier(
        json_dict={
            "fetcher_uuid": fetcher_uuid,
            "amount": 0,
            "length": 0,
            "long_term_part_mode": enum.LONGPART.fqdn_hash,
        }
    )
    count_hash = response["url_frontiers_count"]

    db_hash_count = (
        db.query(db_models.Frontier)
        .filter(db_models.Frontier.fqdn_hash_fetcher_index == 0)
        .count()
    )

    assert count_hash == db_hash_count


# Dev API
def test_get_db_stats():
    response = client.get(c.stats_endpoint)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 8


def test_generate_example_db():
    before = client.get(c.stats_endpoint).json()
    response = client.post(
        c.database_endpoint,
        json={
            "fetcher_amount": 1,
            "fqdn_amount": 1,
            "min_url_amount": 1,
            "max_url_amount": 1,
            "connection_amount": 2,
        },
    )
    sleep(3)
    after = client.get(c.stats_endpoint).json()
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert after["fetcher_amount"] == before["fetcher_amount"] + 1
    assert after["frontier_amount"] == before["frontier_amount"] + 1
    assert after["url_amount"] == before["url_amount"] + 1
    assert after["url_ref_amount"] == before["url_ref_amount"] + 2


def test_generate_example_frontier_wrong_initial_values():
    response = client.post(
        c.database_endpoint,
        json={
            "fetcher_amount": 0,
            "fqdn_amount": 1,
            "min_url_amount": 2,
            "max_url_amount": 1,
            "connection_amount": 1,
            "visited_ratio": 0.0,
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Value 2 is larger than 1"


def test_delete_example_db():
    response = client.delete(
        c.database_endpoint,
        json={
            "delete_reserved_fqdns": True,
            "delete_fetcher_hashes": True,
            "delete_url_refs": True,
            "delete_fetchers": True,
            "delete_urls": True,
            "delete_fqdns": True,
        },
    )
    stats = rest.get_stats()
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert stats["fetcher_amount"] == 0
    assert stats["frontier_amount"] == 0
    assert stats["url_amount"] == 0
    assert stats["url_ref_amount"] == 0
    assert stats["reserved_fqdn_amount"] == 0


def test_get_random_urls():
    client.post(
        c.database_endpoint,
        json={
            "fetcher_amount": 0,
            "fqdn_amount": 10,
            "min_url_amount": 1,
            "max_url_amount": 1,
            "connection_amount": 0,
        },
    )
    full_url_list_response = client.get("urls", json={"amount": 10}).json()

    print(full_url_list_response)
    assert len(full_url_list_response["url_list"]) == 10

    specific_fqdn_response = client.get(
        "urls",
        json={"amount": 1, "fqdn": full_url_list_response["url_list"][0]["fqdn"]},
    ).json()

    assert (
        specific_fqdn_response["url_list"][0]["fqdn"]
        == full_url_list_response["url_list"][0]["fqdn"]
    )


def test_consistent_hashing_uniformly_distributed():
    fetcher_amount = 10
    fqdn_amount = 250

    rest.delete_full_database(full=True)
    rest.create_database(fetcher_amount=fetcher_amount, fqdn_amount=fqdn_amount)

    fetcher_hashes = database.get_fetcher_hashes(db)
    hashes_sorted = sorted(fetcher_hashes, key=lambda k: k["hash"])

    fetcher_hash_range = []
    for i in range(len(hashes_sorted) - 1):
        fetcher_hash_range.append(
            dict(
                uuid=hashes_sorted[i]["uuid"],
                min_hash=hashes_sorted[i]["hash"],
                max_hash=hashes_sorted[i + 1]["hash"],
            )
        )
    fetcher_hash_range.append(
        dict(
            uuid=hashes_sorted[-1]["uuid"],
            min_hash=hashes_sorted[-1]["hash"],
            max_hash=hashes_sorted[0]["hash"],
        )
    )

    fetcher_hash_range_sorted_by_min_hash = sorted(
        fetcher_hash_range, key=lambda k: k["min_hash"]
    )

    for fetcher_hash_range in fetcher_hash_range_sorted_by_min_hash:
        if fetcher_hash_range["min_hash"] < fetcher_hash_range["max_hash"]:
            fetcher_hash_range["url_count"] = (
                db.query(func.count(db_models.Frontier.fqdn)).filter(
                    and_(
                        db_models.Frontier.fqdn_hash >= fetcher_hash_range["min_hash"],
                        db_models.Frontier.fqdn_hash < fetcher_hash_range["max_hash"],
                    )
                )
            ).first()[0]
        else:
            fetcher_hash_range["url_count"] = (
                db.query(func.count(db_models.Frontier.fqdn))
                .filter(
                    or_(
                        db_models.Frontier.fqdn_hash >= fetcher_hash_range["min_hash"],
                        db_models.Frontier.fqdn_hash < fetcher_hash_range["max_hash"],
                    )
                )
                .first()[0]
            )

    return_list = defaultdict(int)
    for d in fetcher_hash_range_sorted_by_min_hash:
        return_list[d['uuid']] += d['url_count']

    group_summed_hash_list = [{'id': id_, 'count': count_} for id_, count_ in return_list.items()]

    url_counts = [f["count"] for f in group_summed_hash_list]

    assert (
        len(fetcher_hash_range_sorted_by_min_hash) == fetcher_amount * c.ch_hash_amount
    )
    mean = sum(url_counts) / len(url_counts)
    variance = sum((xi - mean) ** 2 for xi in url_counts) / len(url_counts)

    assert variance <= 5 * mean
