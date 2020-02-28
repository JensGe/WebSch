from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_frontier():
    response = client.post(
        "/frontiers/",
        json={
            "crawler_uuid": "12345678-90ab-cdef-0000-000000000000",
            "amount": 2,
            "length": 0
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

