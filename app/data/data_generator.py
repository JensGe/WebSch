import random
import string
import csv
import zlib
import hashlib
import xxhash


# def generate_hash_zlib(text: str):
#     return zlib.crc32(str.encode(text)) & 0xffffffff


def generate_hash(text: str, seed: int = 0) -> int:
    int_hash = xxhash.xxh64(str.encode(text), seed=seed).intdigest()
    return int_hash % 9223372036854775807


def generate_hash_hashlib_md5(text: str) -> int:
    byte_hash = hashlib.md5(str.encode(text)).digest()
    int_hash = int.from_bytes(byte_hash, "big")
    return int_hash % 32767


def random_text(length: int = None, language: str = "de"):

    chars = string.ascii_lowercase
    if length is None:
        length = random.randint(10, 16)

    if language == "de":
        distribution = [
            6.51,
            1.89,
            3.06,
            5.08,
            17.40,
            1.66,
            3.01,
            4.76,
            7.55,
            0.27,
            1.21,
            3.44,
            2.53,
            9.78,
            2.51,
            0.79,
            0.02,
            7.00,
            7.27,
            6.15,
            4.35,
            0.67,
            1.89,
            0.03,
            0.04,
            1.13,
        ]

    elif language == "se":
        distribution = [
            9.3,
            1.3,
            1.3,
            4.5,
            9.9,
            2.0,
            3.3,
            2.1,
            5.1,
            0.7,
            3.2,
            5.2,
            3.5,
            8.8,
            4.1,
            1.7,
            0.007,
            8.3,
            6.3,
            8.7,
            1.8,
            2.4,
            0.03,
            0.1,
            0.6,
            0.02,
        ]

    elif language == "fr":
        distribution = [
            7.636,
            0.901,
            3.260,
            3.669,
            14.715,
            1.066,
            0.866,
            0.737,
            7.529,
            0.545,
            0.049,
            5.456,
            2.968,
            7.095,
            5.378,
            3.021,
            1.362,
            6.553,
            7.948,
            7.244,
            6.311,
            1.628,
            0.114,
            0.387,
            0.308,
            0.136,
        ]

    elif language == "es":
        distribution = [
            12.53,
            1.42,
            4.68,
            5.86,
            13.68,
            0.69,
            1.01,
            0.70,
            6.25,
            0.44,
            0.00,
            4.97,
            3.15,
            6.71,
            8.68,
            2.51,
            0.88,
            6.87,
            7.98,
            4.63,
            3.93,
            0.90,
            0.02,
            0.22,
            0.90,
            0.52,
        ]

    elif language == "it":
        distribution = [
            11.74,
            0.92,
            4.5,
            3.73,
            11.79,
            0.95,
            1.64,
            1.54,
            11.28,
            0.00,
            0.00,
            6.51,
            2.51,
            6.88,
            9.83,
            3.05,
            0.51,
            6.37,
            4.98,
            5.62,
            3.01,
            2.10,
            0.00,
            0.00,
            0.00,
            0.49,
        ]
    else:  # english
        distribution = [
            8.167,
            1.492,
            2.782,
            4.253,
            12.702,
            2.228,
            2.015,
            6.094,
            6.966,
            0.153,
            0.772,
            4.025,
            2.406,
            6.749,
            7.507,
            1.929,
            0.095,
            5.987,
            6.327,
            9.056,
            2.758,
            0.978,
            2.360,
            0.150,
            1.974,
            0.074,
        ]

    return "".join(random.choices(population=chars, weights=distribution, k=length))


def random_pagerank(rank: int = random.randint(0, 60000000000)):
    if rank <= 10:
        random_pagerank = random.uniform(8.0, 10.0)
    elif rank <= 100:
        random_pagerank = random.uniform(4.0, 8.0)
    elif rank <= 1000:
        random_pagerank = random.uniform(2.0, 4.0)
    elif rank <= 10000:
        random_pagerank = random.uniform(1.0, 2.0)
    elif rank <= 100000:
        random_pagerank = random.uniform(0.2, 1.0)
    elif rank <= 1000000:
        random_pagerank = random.uniform(0.01, 0.2)
    elif rank <= 10000000:
        random_pagerank = random.uniform(0.001, 0.01)
    elif rank <= 100000000:
        random_pagerank = random.uniform(0.0001, 0.001)
    elif rank <= 1000000000:
        random_pagerank = random.uniform(0.00001, 0.0001)
    else:
        random_pagerank = random.uniform(0.000001, 0.00001)

    return random_pagerank


def random_tld(top: int = 0):

    with open("app/data/top200_tlds.csv", "r") as file:
        reader = csv.reader(file)
        tld_dist = [(row[0], int(row[1])) for row in reader]
        tlds, dist = map(list, zip(*tld_dist))

    if top == 0 or top >= len(tlds):
        return random.choices(population=tlds, weights=dist, k=1)[0]
    else:
        return random.choices(population=tlds[:top], weights=dist[:top], k=1)[0]


def random_crawl_delay():
    crawl_delays = [
        None,
        1,
        2,
        3,
        5,
        10,
        15,
        20,
        30,
        45,
        50,
        60,
        120,
        200,
        300,
        600,
        1000,
    ]
    distibution = [
        0.80000,
        0.00800,
        0.00450,
        0.00450,
        0.01950,
        0.05400,
        0.00450,
        0.01900,
        0.01500,
        0.00800,
        0.00100,
        0.01800,
        0.00800,
        0.00450,
        0.00300,
        0.00150,
        0.00080,
    ]

    return random.choices(population=crawl_delays, weights=distibution)[0]

