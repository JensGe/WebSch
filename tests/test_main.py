from starlette.testclient import TestClient
from starlette import status

from app.main import app
from app.database import crud
from app.database.database import SessionLocal


client = TestClient(app)


def test_get_all_crawler():
    crud.delete_crawlers(SessionLocal())
    client.post("/crawlers/", json={"contact": "jens@honzont.de", "name": "IsaacV"})
    client.post("/crawlers/", json={"contact": "jens@honzont.de", "name": "IsaacVI"})
    json_response = client.get("/crawlers/").json()
    assert len(json_response) == 2


def test_create_crawler():
    crud.delete_crawlers(SessionLocal())
    response = client.post(
        "/crawlers/",
        json={
            "contact": "jens@honzont.de",
            "name": "IsaacIV",
            "location": "Germany",
            "tld_preference": "de",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_create_crawler_duplicate():
    crud.delete_crawlers(SessionLocal())
    client.post("/crawlers/", json={"contact": "jens@honzont.de", "name": "IsaacIV"})
    response2 = client.post(
        "/crawlers/", json={"contact": "jens@honzont.de", "name": "IsaacIV"}
    )
    assert response2.status_code == status.HTTP_409_CONFLICT


def test_update_crawler():
    crud.delete_crawlers(SessionLocal())
    create_response = client.post(
        "/crawlers/",
        json={"contact": "jens@honzont.de", "name": "IsaacIV", "location": "Germany"},
    ).json()
    uuid = create_response["uuid"]
    contact = create_response["contact"]
    name = "IsaacXII"
    update_response = client.put(
        "/crawlers/", json={"uuid": uuid, "contact": contact, "name": name}
    )
    assert update_response.status_code == status.HTTP_200_OK
    assert update_response.json()["location"] is None


def test_patch_crawler():
    crud.delete_crawlers(SessionLocal())
    create_response = client.post(
        "/crawlers/",
        json={
            "contact": "jens@honzont.de",
            "name": "IsaacIV",
            "location": "Germany",
            "tld_preference": "de",
        },
    ).json()
    uuid = create_response["uuid"]
    name = "IsaacIX"

    update_response = client.patch(
        "/crawlers/", json={"uuid": uuid, "name": name}
    )
    assert update_response.status_code == status.HTTP_200_OK
    assert update_response.json()["location"] == "Germany"
    assert update_response.json()["name"] == "IsaacIX"


def test_delete_crawler():
    crud.delete_crawlers(SessionLocal())
    json_response = client.post(
        "/crawlers/", json={"contact": "jens@honzont.de", "name": "IsaacVII"}
    ).json()
    created_uuid = json_response["uuid"]
    print("UUID: {}".format(created_uuid))
    delete_response = client.delete("/crawlers/", json={"uuid": created_uuid})

    assert delete_response.status_code == status.HTTP_204_NO_CONTENT
    assert delete_response.content == b''

    json_response = client.get("/crawlers/").json()
    assert len(json_response) == 0


def test_delete_crawler_not_found():
    assert 1 == 0
    # ToDo test_delete_crawler_not_found()


def test_update_crawler_bad_uuid():
    crud.delete_crawlers(SessionLocal())
    client.post("/crawlers/", json={"contact": "jens@honzont.de", "name": "IsaacIV"})
    assert 1 == 0
    # ToDo test_update_crawler_bad_uuid


def test_update_crawler_no_unique_contact_name_combination():
    assert 1 == 0
    # ToDo test_update_crawler_no_unique_contact_name_combination()


# ToDo Check: This is old stuff
def test_get_frontier():
    response = client.post(
        "/frontiers/",
        json={
            "crawler_uuid": "12345678-90ab-cdef-0000-000000000000",
            "amount": 2,
            "length": 0,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "amount": 2,
        "response_url": "http://www.example.com/submit",
        "url_lists": [
            {
                "length": 0,
                "tld": None,
                "fqdn": "http://www.example.com",
                "ipv4": "127.0.0.1",
                "urls": [],
            },
            {
                "length": 0,
                "tld": None,
                "fqdn": "http://www.example.com",
                "ipv4": "127.0.0.1",
                "urls": [],
            },
        ],
    }


def test_get_frontier_bad_uuid():
    response = client.post(
        "/frontiers/",
        json={
            "crawler_uuid": "12345678-90ab-cdef-0000-000000000001",
            "amount": 2,
            "length": 0,
        },
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Crawler UUID 12345678-90ab-cdef-0000-000000000001 not Found, please register at /crawler/"
    }
