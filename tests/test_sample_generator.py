from app.database import sample_generator


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


def test_get_tld_from_fqdn():
    fqdn_1 = "www.xyz.com"
    assert "com" == sample_generator.get_tld_from_fqdn(fqdn_1)


