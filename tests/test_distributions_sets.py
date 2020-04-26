from app.common import distribution_sets as dist_gen


def test_get_random_pagerank():
    rand_rank = dist_gen.get_random_pagerank()

    assert isinstance(rand_rank, float)


def test_get_random_tld():
    tld = dist_gen.get_random_tld()

    assert isinstance(tld, str)
    assert len(tld) > 1
