# === api_client/client.py ===

import logging
import requests
from typing import Optional, Any, Dict
from .auth import Authenticator
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class APIClient:
    def __init__(self, base_url: str, auth: Authenticator):
        self.base_url = base_url.rstrip('/')
        self.auth = auth
        self.session = requests.Session()

        # Retry config
        retries = Retry(
            total=3,
            backoff_factor=0.3,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def _get_headers(self) -> Dict[str, str]:
        token = self.auth.get_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def _request(self, method: str, endpoint: str, **kwargs) -> Optional[Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self._get_headers()
        kwargs.setdefault("headers", headers)

        try:
            response = self.session.request(method, url, **kwargs)

            # If token expired, re-authenticate and retry once
            if response.status_code == 401:
                logger.warning("Received 401. Attempting re-authentication...")
                if self.auth.force_relogin():
                    headers = self._get_headers()
                    kwargs["headers"] = headers
                    response = self.session.request(method, url, **kwargs)
                else:
                    logger.error("Re-authentication failed.")
                    return None

            response.raise_for_status()
            if response.content:
                return response.json()
            return None

        except requests.RequestException as e:
            logger.exception(f"Request to {url} failed.")
            return None

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Any]:
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> Optional[Any]:
        return self._request("POST", endpoint, json=json)

    def put(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> Optional[Any]:
        return self._request("PUT", endpoint, json=json)

    def delete(self, endpoint: str) -> Optional[Any]:
        return self._request("DELETE", endpoint)
