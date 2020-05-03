from app.common import random_data_generator as rand_gen
from app.data import data_generator as data_gen
from app.common import enum
import string
import datetime


def test_get_random_hex():
    avail_char = "0123456789ABCDEF"
    rnd_hex_list = []
    for _ in range(50):
        rnd_hex_list.append(rand_gen.random_hex())
    error = True
    for item in rnd_hex_list:
        if avail_char.find(item) == -1:
            error = False
    assert error is True


def test_get_random_example_ipv6():
    rand_ipv6 = rand_gen.random_example_ipv6()
    assert len(rand_ipv6) == 14


def test_get_german_text():
    text_length = 7
    random_text = data_gen.random_text(text_length)
    assert len(random_text) == text_length


def test_get_random_academic_name():
    academic_name = rand_gen.random_academic_name()
    name, number = academic_name.split(" ")
    assert name in enum.ACADEMICS.__members__.values()
    assert name.istitle()
    non_roman_chars = ''.join(c for c in string.ascii_uppercase if c not in 'CDILMVX')
    for char in non_roman_chars:
        assert char not in number


def test_get_random_urls():
    random_url_list = rand_gen.random_urls("www.xyz.com", 1000)
    assert type(random_url_list) == list
    assert len(random_url_list) == 1000


def test_get_random_datetime():
    gen_datetime = rand_gen.random_datetime()
    assert type(gen_datetime) == datetime.datetime
