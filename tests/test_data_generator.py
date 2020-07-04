from app.data import data_generator as data_gen
from app.common import random_data_generator as rand_gen
from app.database import sample_generator as sam_gen
from app.database import pyd_models as pyd
from datetime import datetime
from uuid import uuid4


def test_get_random_pagerank():
    rand_rank = data_gen.random_pagerank()
    assert isinstance(rand_rank, float)


def test_get_high_pagerank():
    pagerank10 = data_gen.random_pagerank(rank=5)
    pagerank100 = data_gen.random_pagerank(rank=50)
    pagerank1k = data_gen.random_pagerank(rank=500)
    pagerank10k = data_gen.random_pagerank(rank=5000)
    pagerank100k = data_gen.random_pagerank(rank=50000)
    pagerank1ml = data_gen.random_pagerank(rank=500000)
    pagerank10ml = data_gen.random_pagerank(rank=5000000)
    pagerank100ml = data_gen.random_pagerank(rank=50000000)
    pagerank1mr = data_gen.random_pagerank(rank=500000000)
    pagerank15mr = data_gen.random_pagerank(rank=10000000000)

    assert 8.0 <= pagerank10 <= 10.0
    assert 4.0 <= pagerank100 <= 8.0
    assert 2.0 <= pagerank1k <= 4.0
    assert 1.0 <= pagerank10k <= 2.0
    assert 0.2 <= pagerank100k <= 1.0
    assert 0.01 <= pagerank1ml <= 0.2
    assert 0.001 <= pagerank10ml <= 0.01
    assert 0.0001 <= pagerank100ml <= 0.001
    assert 0.00001 <= pagerank1mr <= 0.0001
    assert 0.0 <= pagerank15mr <= 0.00001


def test_get_random_tld():
    tld = data_gen.random_tld()

    assert isinstance(tld, str)
    assert len(tld) > 1


def test_get_random_crawl_delay():
    crawl_delay_list = [data_gen.random_crawl_delay() for _ in range(200)]
    print(crawl_delay_list)
    assert isinstance(crawl_delay_list[0], int) or crawl_delay_list[0] is None


def test_avg_dates():
    request = pyd.GenerateRequest(visited_ratio=0.5)
    fqdn = rand_gen.get_random_fqdn()
    url_list = rand_gen.random_urls(fqdn, 10)
    fqdn_url_list = [sam_gen.new_url(url_list[i], fqdn, request) for i in range(10)]

    avg_date = sam_gen.avg_dates(fqdn_url_list)
    print(avg_date)
    assert isinstance(avg_date, datetime)
