# === api_client/async_client.py ===

import logging
from typing import Optional, Dict, List, Any

import httpx
import backoff
from .auth import Authenticator
from models.generic import ApiResponse
from models.user import UserProfile
from models.organization import Organization

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class AsyncAPIClient:
    def __init__(self, base_url: str, auth: Authenticator):
        self.base_url = base_url.rstrip("/")
        self.auth = auth
        self.client = httpx.AsyncClient()

    def _get_headers(self) -> Dict[str, str]:
        token = self.auth.get_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    @backoff.on_exception(
        backoff.expo,
        (httpx.ConnectError, httpx.ReadTimeout, httpx.RemoteProtocolError),
        max_tries=3
    )
    async def _request(self, method: str, endpoint: str, **kwargs) -> Optional[Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self._get_headers()
        kwargs.setdefault("headers", headers)

        try:
            response = await self.client.request(method, url, **kwargs)

            if response.status_code == 401:
                logger.warning("Received 401. Attempting re-authentication...")
                if self.auth.force_relogin():
                    headers = self._get_headers()
                    kwargs["headers"] = headers
                    response = await self.client.request(method, url, **kwargs)
                else:
                    logger.error("Re-authentication failed.")
                    return None

            response.raise_for_status()

            if response.content:
                return response.json()
            return None

        except httpx.RequestError as e:
            logger.exception(f"Async request to {url} failed.")
            return None

    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Any]:
        return await self._request("GET", endpoint, params=params)

    async def post(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> Optional[Any]:
        return await self._request("POST", endpoint, json=json)

    async def put(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> Optional[Any]:
        return await self._request("PUT", endpoint, json=json)

    async def delete(self, endpoint: str) -> Optional[Any]:
        return await self._request("DELETE", endpoint)

    async def getUserProfile(self) -> Optional[Any]:
        endpoint = "api/ov/v1/user/profile"
        rawResponse = await self.get(endpoint)
        response = ApiResponse[UserProfile].model_validate(rawResponse)
        return response   

    async def updateUserProfile(self, userProfile: UserProfile) -> Optional[Any]:
        endpoint = "api/ov/v1/user/profile"
        # Convert model to dict instead of JSON string for use with httpx
        userProfileDict = userProfile.model_dump(mode="json")
        rawResponse = await self.put(endpoint, json=userProfileDict)
        if rawResponse:
            return ApiResponse[UserProfile].model_validate(rawResponse)
        return rawResponse

    async def createAnOrganization(self, organization: Organization) -> Optional[Any]:
        endpoint = "api/ov/v1/organizations"
        rawResponse = await self.post(endpoint, organization)
        if rawResponse:
            return ApiResponse[Organization].model_validate(rawResponse)
        return rawResponse          

    async def getAllUserOrganizations(self) -> Optional[Any]:
        endpoint = "api/ov/v1/organizations"
        rawResponse = await self.get(endpoint)
        if rawResponse:
            return ApiResponse[List[Organization]   ].model_validate(rawResponse)
        return rawResponse           
        
    async def close(self):
        await self.client.aclose()
