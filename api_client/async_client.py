# === api_client/async_client.py ===

import logging
from typing import Optional, Dict, List, Any

import httpx
import backoff
from .auth import Authenticator
from models.generic import ApiResponse
from models.user import UserProfile
from models.organization import Organization
from models.site import Site
from models.device import Device


from utilities.model_validator import safe_model_validate

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class OVCirrusApiClient:
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
        max_tries=2
    )

    async def _request(self, method: str, endpoint: str, **kwargs) -> Optional[Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self._get_headers()
        kwargs.setdefault("headers", headers)

        try:
            response = await self.client.request(method, url, **kwargs)

            # Handle 401 Unauthorized and attempt re-authentication
            if response.status_code == 401:
                logger.warning("Received 401. Attempting re-authentication...")
                if self.auth.force_relogin():
                    headers = self._get_headers()
                    kwargs["headers"] = headers
                    response = await self.client.request(method, url, **kwargs)
                else:
                    logger.error("Re-authentication failed. Exiting.")
                    return None  # Return None after max retries or failure

            response.raise_for_status()

            if response.content:
                try:
                    return response.json()
                except Exception as e:
                    logger.warning(f"Failed to decode JSON from response: {e}")
                    return None
            return None

        except httpx.HTTPStatusError as e:
            logger.warning(f"HTTP error {e.response.status_code}: {e.response.text}")
            return e.response.json()  # Return error details to be handled by the caller
        except Exception as e:
            logger.exception(f"Unhandled exception during API request: {e}")
            raise  # Reraise exception if it's unexpected



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
        return safe_model_validate(ApiResponse[UserProfile], rawResponse)

    async def updateUserProfile(self, userProfile: UserProfile) -> Optional[Any]:
        endpoint = "api/ov/v1/user/profile"
        rawResponse = await self.put(endpoint, userProfile.model_dump(mode="json"))
        if rawResponse:
            return safe_model_validate(ApiResponse[UserProfile], rawResponse)
        return rawResponse

    async def createAnOrganization(self, organization: Organization) -> Optional[Any]:
        endpoint = "api/ov/v1/organizations"
        rawResponse = await self.post(endpoint, organization)
        if rawResponse:
            return safe_model_validate(ApiResponse[Organization], rawResponse)
        return rawResponse          

    async def getAllUserOrganizations(self) -> Optional[Any]:
        endpoint = "api/ov/v1/organizations"
        rawResponse = await self.get(endpoint)
        if rawResponse:
            return safe_model_validate(ApiResponse[List[Organization]], rawResponse)
        return rawResponse           

    async def getOrganizationBasicSettings(self, orgId: str) -> Optional[Any]:
        endpoint = "api/ov/v1/organizations/" + orgId + "/settings/basic"
        rawResponse = await self.get(endpoint)
        if rawResponse:
            return safe_model_validate(ApiResponse[Organization], rawResponse)
        return rawResponse          

    async def getOrganization(self, orgId: str) -> Optional[Any]:
        endpoint = "api/ov/v1/organizations/" + orgId
        rawResponse = await self.get(endpoint)
        if rawResponse:
            return safe_model_validate(ApiResponse[Organization], rawResponse)
        return rawResponse        

    async def updateOrganization(self, orgId: str, organization: Organization) -> Optional[Any]:
        endpoint = "api/ov/v1/organizations/" + orgId
        rawResponse = await self.put(endpoint, organization.model_dump(mode="json"))
        if rawResponse:
            return safe_model_validate(ApiResponse[Organization], rawResponse)
        return rawResponse      

    async def deleteOrganization(self, orgId: str) -> Optional[Any]:
        endpoint = "api/ov/v1/organizations/" + orgId
        rawResponse = await self.delete(endpoint)
        if rawResponse:
            try:
                return ApiResponse[Any].model_validate(rawResponse)
            except:
                return None
        return rawResponse           

    async def createSite(self, orgId:str, site: Site) -> Optional[Any]:
        endpoint = "api/ov/v1/organizations/" + orgId + "/sites"
        rawResponse = await self.post(endpoint, site)
        if rawResponse:
            return safe_model_validate(ApiResponse[Site], rawResponse)
        return rawResponse      

    async def getOrganizationSites(self, orgId:str) -> Optional[Any]:
        endpoint = "api/ov/v1/organizations/" + orgId + "/sites"
        rawResponse = await self.get(endpoint)
        if rawResponse:
            return safe_model_validate(ApiResponse[List[Site]], rawResponse)
        return rawResponse       

    async def getOrganizationSitesBuildingsFloors(self, orgId:str) -> Optional[Any]:
        endpoint = "api/ov/v1/organizations/" + orgId + "/sites/buildings/floors"
        rawResponse = await self.get(endpoint)
        if rawResponse:
            return safe_model_validate(ApiResponse[List[Site]], rawResponse)
        return rawResponse            

    async def getSite(self, orgId:str, siteId:str) -> Optional[Any]:
        endpoint = "api/ov/v1/organizations/" + orgId + "/sites/" siteId
        rawResponse = await self.get(endpoint)
        if rawResponse:
            return safe_model_validate(ApiResponse[Site], rawResponse)
        return rawResponse   

    async def updateSite(self, orgId: str, siteId: str, site:Site) -> Optional[Any]:
        endpoint = "api/ov/v1/organizations/" + orgId + "/sites/" siteId
        rawResponse = await self.put(endpoint, site.model_dump(mode="json"))
        if rawResponse:
            return safe_model_validate(ApiResponse[Site], rawResponse)
        return rawResponse            

    async def deleteSite(self, orgId: str, siteId: str) -> Optional[Any]:
        endpoint = "api/ov/v1/organizations/" + orgId + "/sites/" siteId
        rawResponse = await self.delete(endpoint)
        if rawResponse:
            try:
                return ApiResponse[Any].model_validate(rawResponse)
            except:
                return None
        return rawResponse 

    async def createDevice(self, orgId:str, siteId: str, device:Device) -> Optional[Any]:
        endpoint = "api/ov/v1/organizations/" + orgId + "/sites/" + siteId + "/devices"
        rawResponse = await self.post(endpoint, device)
        if rawResponse:
            return safe_model_validate(ApiResponse[Device], rawResponse)
        return rawResponse      

    async def getAllDevices(self, orgId:str, site:str) -> Optional[Any]:
        endpoint = "api/ov/v1/organizations/" + orgId + "/sites/" + siteId + "/devices"
        rawResponse = await self.get(endpoint)
        if rawResponse:
            return safe_model_validate(ApiResponse[List[Site]], rawResponse)
        return rawResponse   

    async def createRemoteAP(self, orgId:str, siteId: str, device:Device) -> Optional[Any]:
        endpoint = "api/ov/v1/organizations/" + orgId + "/sites/" + siteId + "/remote-aps"
        rawResponse = await self.post(endpoint, device)
        if rawResponse:
            return safe_model_validate(ApiResponse[Device], rawResponse)
        return rawResponse  

    async def getAllDevicesFromOrganization(self, orgId:str) -> Optional[Any]:
        endpoint = "api/ov/v1/organizations/" + orgId + "/sites/devices"
        rawResponse = await self.get(endpoint)
        if rawResponse: 
            return safe_model_validate(ApiResponse[List[Site]], rawResponse)
        return rawResponse        

    async def getDevice(self, orgId:str, deviceId: str) -> Optional[Any]:
        endpoint = "api/ov/v1/organizations/" + orgId + "/devices/" + deviceId
        rawResponse = await self.get(endpoint)
        if rawResponse: 
            return safe_model_validate(ApiResponse[DeviceData], rawResponse)
        return rawResponse               

    async def getDeviceDetails(self, orgId:str, deviceId: str) -> Optional[Any]:
        endpoint = "api/ov/v1/organizations/" + orgId + "/devices/" + deviceId + "/details"
        rawResponse = await self.get(endpoint)
        if rawResponse: 
            return safe_model_validate(ApiResponse[Device], rawResponse)
        return rawResponse   

    async def updateDevice(self, orgId: str, siteId: str, deviceId:str, device:Device) -> Optional[Any]:
        endpoint = "api/ov/v1/organizations/" + orgId + "/sites/" siteId + "/devices/" + deviceId
        rawResponse = await self.put(endpoint, device.model_dump(mode="json"))
        if rawResponse:
            return safe_model_validate(ApiResponse[Device], rawResponse)
        return rawResponse      

    async def deleteDevice(self, orgId: str, siteId: str, deviceId:str) -> Optional[Any]:
        endpoint = "api/ov/v1/organizations/" + orgId + "/sites/" siteId + "/devices/" + deviceId
        rawResponse = await self.delete(endpoint)
        if rawResponse:
            try:
                return ApiResponse[Any].model_validate(rawResponse)
            except:
                return None
        return rawResponse  

    async def updateRemoteAP(self, orgId: str, siteId: str, deviceId:str, device:Device) -> Optional[Any]:
        endpoint = "api/ov/v1/organizations/" + orgId + "/sites/" siteId + "/remote-aps/" + deviceId
        rawResponse = await self.put(endpoint, device.model_dump(mode="json"))
        if rawResponse:
            return safe_model_validate(ApiResponse[Device], rawResponse)
        return rawResponse                                        
        
    async def close(self):
        await self.client.aclose()
