from enum import Enum


class LTF(str, Enum):
    """
    Long Term Frontier Strategy
    """
    random = "random"
    top_level_domain = "top_level_domain"
    large_sites_first = "large_sites_first"
    small_sites_first = "small_sites_first"
    old_sites_first = "old_sites_first"
    new_sites_first = "new_sites_first"
    avg_pagerank = "avg_pagerank"
    avg_change_rate = "avg_change_rate"
    fqdn_hash = "fqdn_hash"
    consistent_hashing = "consistent_hashing"


class STF(str, Enum):
    """
    Short Term Frontier Strategy
    """
    random = "random"
    old_pages_first = "old_pages_first"
    new_pages_first = "new_pages_first"
    pagerank = "pagerank"
    change_rate = "change_rate"


class LPPDISTR(str, Enum):
    """
    Links per Page Distribution Type
    """
    discrete = "discrete"
    linear_smaller = "linear_smaller"
    power_law = "power_law"


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
