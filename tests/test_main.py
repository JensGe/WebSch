from fastapi.testclient import TestClient
from fastapi import status

from app.main import app
from app.common import defaults
from app.database import crud, database


client = TestClient(app)
db = database.SessionLocal()

# reusables
test_email_1 = "jens@honzont.de"
crawler_endpoint = "/crawlers/"
database_endpoint = "/database/"
stats_endpoint = "/stats/"


def test_get_all_crawler():
    crud.delete_crawlers(db)
    client.post(crawler_endpoint, json={"contact": test_email_1, "name": "IsaacV"})
    client.post(crawler_endpoint, json={"contact": test_email_1, "name": "IsaacVI"})
    json_response = client.get(crawler_endpoint).json()
    assert len(json_response) == 2


def test_create_crawler():
    crud.delete_crawlers(db)
    response = client.post(
        crawler_endpoint,
        json={
            "contact": "jens@honzont.de",
            "name": "IsaacIV",
            "location": "Germany",
            "tld_preference": "de",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_create_crawler_duplicate():
    crud.delete_crawlers(db)
    client.post(crawler_endpoint, json={"contact": test_email_1, "name": "IsaacIV"})
    response2 = client.post(
        crawler_endpoint, json={"contact": test_email_1, "name": "IsaacIV"}
    )
    assert response2.status_code == status.HTTP_409_CONFLICT


def test_update_crawler():
    crud.delete_crawlers(db)
    create_response = client.post(
        crawler_endpoint,
        json={"contact": test_email_1, "name": "IsaacIV", "location": "Germany"},
    ).json()
    uuid = create_response["uuid"]
    contact = create_response["contact"]
    name = "IsaacXII"
    update_response = client.put(
        crawler_endpoint, json={"uuid": uuid, "contact": contact, "name": name}
    )
    assert update_response.status_code == status.HTTP_200_OK
    assert update_response.json()["location"] is None


def test_patch_crawler():
    crud.delete_crawlers(db)
    create_response = client.post(
        crawler_endpoint,
        json={
            "contact": test_email_1,
            "name": "IsaacIV",
            "location": "Germany",
            "tld_preference": "de",
        },
    ).json()
    uuid = create_response["uuid"]
    name = "IsaacIX"

    update_response = client.patch(crawler_endpoint, json={"uuid": uuid, "name": name})
    assert update_response.status_code == status.HTTP_200_OK
    assert update_response.json()["location"] == "Germany"
    assert update_response.json()["name"] == "IsaacIX"


def test_delete_crawler():
    crud.delete_crawlers(db)
    json_response = client.post(
        crawler_endpoint, json={"contact": test_email_1, "name": "IsaacVII"}
    ).json()
    created_uuid = json_response["uuid"]
    print("UUID: {}".format(created_uuid))
    delete_response = client.delete(crawler_endpoint, json={"uuid": created_uuid})

    assert delete_response.status_code == status.HTTP_204_NO_CONTENT
    assert delete_response.content == b""

    json_response = client.get(crawler_endpoint).json()
    assert len(json_response) == 0


def test_get_db_stats():
    response = client.get(stats_endpoint)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 4


def test_generate_example_db():
    before = client.get(stats_endpoint)
    response = client.post(database_endpoint)
    after = client.get(stats_endpoint)
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert after["crawler_amount"] == before["crawler_amount"] + defaults.crawler
    assert after["frontier_amount"] == before["frontier_amount"] + defaults.fqdn
    assert after["url_amount"] > before["url_amount"]


# def test_delete_crawler_not_found():
#     assert 1 == 0
#     # ToDo test_delete_crawler_not_found()
#
#
# def test_update_crawler_bad_uuid():
#     crud.delete_crawlers(SessionLocal())
#     client.post("/crawlers/", json={"contact": "jens@honzont.de", "name": "IsaacIV"})
#     assert 1 == 0
#     # ToDo test_update_crawler_bad_uuid
#
#
# def test_update_crawler_no_unique_contact_name_combination():
#     assert 1 == 0
#     # ToDo test_update_crawler_no_unique_contact_name_combination()
#
#
# # ToDo Check: This is old stuff
# def test_get_frontier():
#     response = client.post(
#         "/frontiers/",
#         json={
#             "crawler_uuid": "12345678-90ab-cdef-0000-000000000000",
#             "amount": 2,
#             "length": 0,
#         },
#     )
#     assert response.status_code == 200
#     assert response.json() == {
#         "amount": 2,
#         "response_url": "http://www.example.com/submit",
#         "url_lists": [
#             {
#                 "length": 0,
#                 "tld": None,
#                 "fqdn": "http://www.example.com",
#                 "ipv4": "127.0.0.1",
#                 "urls": [],
#             },
#             {
#                 "length": 0,
#                 "tld": None,
#                 "fqdn": "http://www.example.com",
#                 "ipv4": "127.0.0.1",
#                 "urls": [],
#             },
#         ],
#     }
#
#
# def test_get_frontier_bad_uuid():
#     response = client.post(
#         "/frontiers/",
#         json={
#             "crawler_uuid": "12345678-90ab-cdef-0000-000000000001",
#             "amount": 2,
#             "length": 0,
#         },
#     )
#     assert response.status_code == 404
#     assert response.json() == {
#         "detail": "Crawler UUID 12345678-90ab-cdef-0000-000000000001 not Found, please register at /crawlers/"
#     }
