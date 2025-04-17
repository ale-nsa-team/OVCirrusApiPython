import pytest
from unittest.mock import AsyncMock
import httpx
from httpx import Response, Request
from api_client.async_client import OVCirrusApiClient
from models.organization import Organization
from models.generic import ApiResponse
from api_client.auth import Authenticator

# Dummy Authenticator that always returns a token
class DummyAuthenticator(Authenticator):
    def get_token(self) -> str:
        return "dummy-token"

    def force_relogin(self) -> bool:
        return True

@pytest.mark.asyncio
async def test_get_organization_valid_response():
    # Mocking a valid response from the API
    raw_response = {
        "status": 200,
        "message": "Success",
        "data": {
            "id": "org123",
            "name": "Test Organization",
            "is2FARequired": True,
            "imageUrl": "http://example.com/image.jpg",
            "countryCode": "US",
            "timezone": "GMT",
            "auditHour": 12,
            "idleTimeout": 60
        }
    }

    # Create an instance of OVCirrusApiClient (replace with actual class)
    obj = OVCirrusApiClient(
        base_url="https://api.example.com",
        auth=DummyAuthenticator()
    )
    
    # Mocking the `get` method to return the raw_response
    obj.get = AsyncMock(return_value=raw_response)

    # Call the method
    result = await obj.getOrganization("org123")

    # Verify the result is an ApiResponse and contains the expected data
    assert isinstance(result, ApiResponse)
    assert isinstance(result.data, Organization)
    assert result.data.id == "org123"
    assert result.data.name == "Test Organization"
    assert result.data.is2FARequired is True
    assert result.data.imageUrl == "http://example.com/image.jpg"

@pytest.mark.asyncio
async def test_get_organization_no_response():
    # Mocking the `get` method to return None
    obj = OVCirrusApiClient(
        base_url="https://api.example.com",
        auth=DummyAuthenticator()
    )
    
    obj.get = AsyncMock(return_value=None)

    # Call the method
    result = await obj.getOrganization("org123")

    # Assert that the result is None because there's no response
    assert result is None

@pytest.mark.asyncio
async def test_get_organization_invalid_status():
    # Mocking an invalid API response (non-200 status code)
    raw_response = {
        "status": 400,
        "message": "Bad Request",
        "data": {}
    }

    # Create an instance of OVCirrusApiClient
    obj = OVCirrusApiClient(
        base_url="https://api.example.com",
        auth=DummyAuthenticator()
    )
    
    # Mock the `get` method to return the raw_response
    obj.get = AsyncMock(return_value=raw_response)

    # Call the method
    result = await obj.getOrganization("org123")

    # Assert that the result is None because the status is not 200
    assert result.status is 400
