# bitcoinetl/rpc/request.py
import hashlib
import requests
from urllib.parse import urlparse, urlunparse

_session_cache = {}

def _get_session(endpoint_uri):
    cache_key = hashlib.md5(endpoint_uri.encode('utf-8')).hexdigest()
    if cache_key not in _session_cache:
        _session_cache[cache_key] = requests.Session()
    return _session_cache[cache_key]

def make_post_request(endpoint_uri, data, *args, **kwargs):
    kwargs.setdefault('timeout', 10)
    session = _get_session(endpoint_uri)
    
    # Parse the URI to extract authentication details
    parsed_uri = urlparse(endpoint_uri)
    auth = None
    if parsed_uri.username and parsed_uri.password:
        auth = (parsed_uri.username, parsed_uri.password)
        # Reconstruct the URI without authentication details
        netloc = parsed_uri.hostname
        if parsed_uri.port:
            netloc += f":{parsed_uri.port}"
        cleaned_uri = urlunparse((
            parsed_uri.scheme,
            netloc,
            parsed_uri.path,
            parsed_uri.params,
            parsed_uri.query,
            parsed_uri.fragment
        ))
    else:
        cleaned_uri = endpoint_uri

    response = session.post(cleaned_uri, data=data, auth=auth, *args, **kwargs)
    response.raise_for_status()
    return response.content
