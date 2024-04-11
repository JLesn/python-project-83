from urllib.parse import urlparse
from validators import url as url_validator


def normalize_url(url):
    norm = urlparse(url)
    return norm.scheme + "://" + norm.netloc


def is_valid(url):
    errors = []
    if url == "":
        errors.append("missing url")
    if url_validator(url) is not True:
        errors.append("incorrect url")
    return errors
