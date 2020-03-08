from app.common import random_data_generator as rand_gen


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


def test_get_random_ipv6():
    rand_ipv6 = rand_gen.get_random_ipv6()
    print(rand_ipv6)
    assert len(rand_ipv6) == 14


def test_get_german_text():
    text_length = 7
    random_text = rand_gen.get_random_german_text(text_length)
    print(random_text)
    assert len(random_text) == text_length



