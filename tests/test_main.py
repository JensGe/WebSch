from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_crawler():
    response = client.post(
        "/crawler/",
        json={
            "contact": "jens@honzont.de",
            "location": "Germany",
            "tld_preference": "de",
        },
    )
    assert response.status_code == 201


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
