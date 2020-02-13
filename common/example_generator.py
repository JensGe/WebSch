import random
import string

tlds = ['com', 'de', 'co.uk', 'org', 'fr']


def get_random_chars(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def generate_tld_url_list(amount, tld):
    url_list = []
    if tld == 'all':
        for i in range(amount):
            url = 'http://www.' + get_random_chars(5) + '.' + random.choice(tlds)
            url_list.append({'url': url})
    else:
        for i in range(amount):
            url = 'http://www.' + get_random_chars(5) + '.' + tld
            url_list.append({'url': url})

    return url_list
