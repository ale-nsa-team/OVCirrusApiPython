# === api_client/authentication.py ===

import logging
from typing import Optional, Dict, List, Any, Type
from datetime import datetime
import httpx
import backoff
from .auth import Authenticator
from models.authentication import AuthDetailData, AuthData, AuthResponse, AuthHistoryDetail

from utilities.model_validator import safe_model_validate

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class AuthenticationClient:
    def __init__(self, base_client: 'BaseClient'):
        self.base = base_client
        
    async def getAuthRecords(
        self,
        orgId: str,
        limit: int,
        offset: int,
        startDate: Optional[datetime] = None,
        endDate: Optional[datetime] = None,
        sort: Optional[List[Dict[str, str]]] = None,
        filters: Optional[Dict[str, Any]] = None,
        search: Optional[str] = None
    ) -> Optional[Any]:
        endpoint = f"api/ov/v1/organizations/{orgId}/am/access-records/authentication-online-records"

        # Format query parameters
        query_params = {
            "limit": limit,
            "offset": offset,
            "startDate": startDate if startDate else None,
            "endDate": endDate if endDate else None,
            "sort": sort or [],
            "filters": filters or {},
            "search": search or ""
        }

        # Send the request
        rawResponse = await self.base.get(endpoint, params=query_params)
        if rawResponse:
            return safe_model_validate(AuthResponse[AuthData], rawResponse)
        return None
    
    async def getAuthHistoryRecords(
        self,
        orgId: str,
        limit: int,
        offset: int,
        startDate: Optional[datetime] = None,
        endDate: Optional[datetime] = None,
        sort: Optional[List[Dict[str, str]]] = None,
        filters: Optional[Dict[str, Any]] = None,
        search: Optional[str] = None
    ) -> Optional[Any]:
        endpoint = f"api/ov/v1/organizations/{orgId}/am/access-records/authentication-history-records"

        # Format query parameters
        query_params = {
            "limit": limit,
            "offset": offset,
            "startDate": startDate if startDate else None,
            "endDate": endDate if endDate else None,
            "sort": sort or [],
            "filters": filters or {},
            "search": search or ""
        }

        # Send the request
        rawResponse = await self.base.get(endpoint, params=query_params)
        if rawResponse:
            return safe_model_validate(AuthResponse[AuthData], rawResponse)
        return None    
    
    async def getAuthHistoryRecordDetail(
        self,
        orgId: str,
        recordId: str,
    ) -> Optional[Any]:
        endpoint = f"api/ov/v1/organizations/{orgId}/am/access-records/authentication-history-records/{recordId}"

        # Send the request
        rawResponse = await self.base.get(endpoint)
        if rawResponse:
            return safe_model_validate(AuthResponse[AuthHistoryDetail], rawResponse)
        return None   

    async def getOnlineAuthRecord(
        self,
        orgId: str,
        mac: str,
    ) -> Optional[Any]:
        endpoint = f"api/ov/v1/organizations/{orgId}/am/access-records/authentication-online-records/{mac}"

        # Send the request
        rawResponse = await self.base.get(endpoint)
        if rawResponse:
            return safe_model_validate(AuthResponse[AuthDetailData], rawResponse)
        return None            
    


