from websch.common import example_generator as ex


def test_get_random_chars():
    random3 = ex.get_random_chars(3)
    random10 = ex.get_random_chars(10)

    assert len(random3) == 3
    assert len(random10) == 10


def test_generate_tld_url_list():
    random_list = ex.generate_tld_url_list(10, 'all')

    assert random_list[0]['url'][:11] == 'http://www.'
