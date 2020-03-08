from app.database import sample_generator


# def test_generate_tld_url_list():
#     url_list = sample_generator.generate_tld_url_list(None, 10)
#     assert len(url_list['urls']) == 10
#     assert url_list['urls'][9][:11] == "http://www."
#     # assert random_list[9]["url"][:11] == "http://www."
#
#
# def test_create_url_list():
#     random_collection = sample_generator.generate_frontier("12345678-90ab-cdef-0000-000000000000", 3, 10, "de")
#     assert random_collection['url_lists'][2]['urls'][9][-3:] == ".de"


def test_get_random_hex():
    avail_char = "0123456789abcdefg"
    rnd_hex_list = []
    for _ in range(50):
        rnd_hex_list.append(sample_generator.get_random_hex())
    print(rnd_hex_list)
    error = True
    for item in rnd_hex_list:
        if avail_char.find(item) == -1:
            error = False
    assert error is True


def test_get_random_ipv6():
    rand_ipv6 = sample_generator.get_random_ipv6()
    print(rand_ipv6)
    assert len(rand_ipv6) == 14


def test_get_german_text():
    text_length = 20
    random_text = sample_generator.get_random_german_text(text_length)
    print(random_text)
    assert len(random_text) == text_length
