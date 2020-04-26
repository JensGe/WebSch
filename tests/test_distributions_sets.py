from app.common import distribution_sets as dists
from datetime import datetime


def test_get_random_pagerank():
    begin_time = datetime.now()
    rand_rank = dists.get_random_pagerank()
    diff_time = datetime.now() - begin_time

    print("Random Number: {}".format(str(rand_rank)))
    print("Time Elapsed: {}".format(str(diff_time)))

    assert isinstance(rand_rank, float)
