from app.common import random_data_generator as rand_gen
from app.common import enum
import string


def test_get_random_hex():
    avail_char = "0123456789abcdefg"
    rnd_hex_list = []
    for _ in range(50):
        rnd_hex_list.append(rand_gen.get_random_hex())
    print(rnd_hex_list)
    error = True
    for item in rnd_hex_list:
        if avail_char.find(item) == -1:
            error = False
    assert error is True


def test_get_random_example_ipv6():
    rand_ipv6 = rand_gen.get_random_example_ipv6()
    print(rand_ipv6)
    assert len(rand_ipv6) == 14


def test_get_german_text():
    text_length = 7
    random_text = rand_gen.get_random_german_text(text_length)
    print(random_text)
    assert len(random_text) == text_length


def test_get_random_academic_name():
    academic_name = rand_gen.get_random_academic_name()
    print(academic_name)
    name, number = academic_name.split(" ")
    assert name in enum.ACADEMICS.__members__.values()
    assert name.istitle()
    non_roman_chars = ''.join(c for c in string.ascii_uppercase if c not in 'CDILMVX')
    for char in non_roman_chars:
        assert char not in number


def test_get_random_urls():
    random_url_list = rand_gen.get_random_urls("www.xyz.com", 100000)
    assert type(random_url_list) == list
    assert len(random_url_list) == 100000
