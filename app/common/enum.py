from enum import Enum


class TLD(str, Enum):
    Germany = "de"
    Commercial = "com"
    France = "fr"
    Organisation = "org"
    Sweden = "se"


class PRIO(str, Enum):
    breath_first_search = "bfs"
    indegree = "ind"
    batch_page_rank = "bpr"
    large_sites_first = "lsf"
    old_sites_first = "osf"
    random = "rand"
    change_rate = "chr"
    opic = "opic"
    webfountain = "webf"


class PART(str, Enum):
    top_level_domain = "tld"
    fqdn_hashing = "fqdn"
    consistent_hashing = "ch"
    geo_distance = "geo"
    round_trip_time = "rtt"
    graph_partitioning = "gp"


class ACADEMICS(str, Enum):
    ampere = "Ampere"
    avogadro = "Avogadro"
    bacon = "Bacon"
    bernoulli = "Bernoulli"
    copernicus = "Copernicus"
    curie = "Curie"
    darwin = "Darwin"
    drake = "Drake"
    einstein = "Einstein"
    euler = "Euler"
    fibonacci = "Fibonacci"
    fermat = "Fermat"
    gauss = "Gauss"
    gibbs = "Gibbs"
    hilbert = "Hilbert"
    hopper = "Hopper"
    hawking = "Hawking"
    kepler = "Kepler"
    lovelace = "Lovelace"
    mendel = "Mendel"
    maxwell = "Maxwell"
    newton = "Newton"
    planck = "Planck"



