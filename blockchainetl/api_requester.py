import requests
import time
from threading import Lock
from typing import Any, Dict, Optional, Union

class ApiRequester:
    """
    A class for making API requests while respecting a specified rate limit.

    This class handles GET requests using the requests library.
    It includes rate limiting functionality, ensuring that the number of requests made does not exceed the specified limit per second.
    If the rate limit is about to be exceeded, the class will wait the appropriate amount of time before making the next request.
    
    This class is designed to be thread-safe, allowing it to be used in multi-threaded applications.
    """

    def __init__(self, api_url: str, api_key: Optional[str], rate_limit: float):
        """
        keyword arguments
        api_url (str): The base URL of the API.
        api_key (str): The API key used for authorization.
        rate_limit (int): The maximum number of requests allowed per second.
        """
        self.api_url = api_url
        self.api_key = api_key
        self.rate_limit = rate_limit  # Rate limit in requests per second
        self.last_request_time = None
        self.lock = Lock()
        
    def _make_get_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, Any]] = None, timeout: Union[float, int] = 5):
        with self.lock:
            # Handle rate limiting
            if self.last_request_time:
                elapsed_time = time.time() - self.last_request_time
                wait_time = max(0, 1/self.rate_limit - elapsed_time)
                if wait_time > 0: 
                    time.sleep(wait_time)

            # Make the request
            response = requests.get(f"{self.api_url}/{endpoint}", params=params, headers=headers, timeout=timeout)

            # Update the last request time
            self.last_request_time = time.time()

        response.raise_for_status()

        return response
