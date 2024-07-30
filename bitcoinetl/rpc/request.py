import hashlib
from ratelimit import limits, sleep_and_retry
import requests

_session_cache = {}


def _get_session(endpoint_uri):
    cache_key = hashlib.md5(endpoint_uri.encode('utf-8')).hexdigest()
    if cache_key not in _session_cache:
        _session_cache[cache_key] = requests.Session()
    return _session_cache[cache_key]

CALLS = 250
PERIOD = 1  # seconds

# Due to quicknode rpc limit, we can do max 300 requests per seconds
@sleep_and_retry
@limits(calls=CALLS, period=PERIOD)
def make_post_request(endpoint_uri, data, *args, **kwargs):
    kwargs.setdefault('timeout', 10)
    session = _get_session(endpoint_uri)
    response = session.post(endpoint_uri, data=data, *args, **kwargs)
    response.raise_for_status()

    return response.content
