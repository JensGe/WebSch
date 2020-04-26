from app.common import data_generator as data_gen


def test_get_random_pagerank():
    rand_rank = data_gen.get_random_pagerank()

    assert isinstance(rand_rank, float)


def test_get_random_tld():
    tld = data_gen.get_random_tld()

    assert isinstance(tld, str)
    assert len(tld) > 1
