from starlette.testclient import TestClient

from app.main import app
from app.database import crud
from app.database.database import SessionLocal


client = TestClient(app)


def test_get_all_crawler():
    crud.delete_all_crawler(SessionLocal())
    client.post("/crawler/", json={"contact": "jens@honzont.de", "name": "IsaacV"})
    client.post("/crawler/", json={"contact": "jens@honzont.de", "name": "IsaacVI"})
    json_response = client.get("/crawler/").json()
    assert len(json_response) == 2


def test_create_crawler():
    crud.delete_all_crawler(SessionLocal())
    response = client.post(
        "/crawler/",
        json={
            "contact": "jens@honzont.de",
            "name": "IsaacIV",
            "location": "Germany",
            "tld_preference": "de",
        },
    )
    assert response.status_code == 201


def test_create_crawler_duplicate():
    crud.delete_all_crawler(SessionLocal())
    client.post("/crawler/", json={"contact": "jens@honzont.de", "name": "IsaacIV"})
    response2 = client.post(
        "/crawler/", json={"contact": "jens@honzont.de", "name": "IsaacIV"}
    )
    assert response2.status_code == 409


def test_update_crawler():
    crud.delete_all_crawler(SessionLocal())
    create_response = client.post(
        "/crawler/",
        json={"contact": "jens@honzont.de", "name": "IsaacIV", "location": "Germany"},
    ).json()
    uuid = create_response["uuid"]
    contact = create_response["contact"]
    name = "IsaacXII"
    update_response = client.put(
        "/crawler/", json={"uuid": uuid, "contact": contact, "name": name}
    )
    assert update_response.status_code == 200
    assert update_response.json()["location"] is None


def test_delete_crawler():
    crud.delete_all_crawler(SessionLocal())
    json_response = client.post(
        "/crawler/", json={"contact": "jens@honzont.de", "name": "IsaacVII"}
    ).json()
    created_uuid = json_response["uuid"]
    print("UUID: {}".format(created_uuid))
    delete_response = client.delete("/crawler/", json={"uuid": created_uuid})

    assert delete_response.status_code == 200

    json_response = client.get("/crawler/").json()
    assert len(json_response) == 0


def test_delete_crawler_not_found():
    assert 1 == 0
    # ToDo test_delete_crawler_not_found()


def test_update_crawler_bad_uuid():
    crud.delete_all_crawler(SessionLocal())
    client.post("/crawler/", json={"contact": "jens@honzont.de", "name": "IsaacIV"})
    assert 1 == 0
    # ToDo test_update_crawler_bad_uuid


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
