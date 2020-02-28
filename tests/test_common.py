from app.common import example_generator as ex


def test_generate_tld_url_list():
    url_list = ex.generate_tld_url_list(None, 10)
    assert len(url_list['urls']) == 10
    assert url_list['urls'][9][:11] == "http://www."
    # assert random_list[9]["url"][:11] == "http://www."


def test_create_url_list():
    random_collection = ex.generate_frontier("12345678-90ab-cdef-0000-000000000000", 3, 10, "de")
    assert random_collection['url_lists'][2]['urls'][9][-3:] == ".de"
