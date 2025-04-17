import pytest
from httpx import Response
from api_client.async_client import AsyncAPIClient
from models.organization import Organization
from models.generic import ApiResponse
from api_client.auth import Authenticator
from unittest.mock import AsyncMock
from typing import Optional

# Dummy Authenticator that always returns a token
class DummyAuthenticator(Authenticator):
    def get_token(self) -> str:
        return "dummy-token"

    def force_relogin(self) -> bool:
        return True

# Mock response data for organization settings
mock_org_settings_data = {
    "status": 200,
    "message": "Success",
    "data": {
        "id": "123",
        "name": "ALE",
        "createdAt": "2022-08-04T12:10:38.058Z",
        "updatedAt": "2022-09-08T15:56:53.407Z",
        "enforceStrongPassword": True,
        "enforceStrongPasswordNotifyType": "SHOW_MESSAGE_AFTER_LOGIN",
        "timezone": "Europe/Tirane",
        "auditHour": 130,
        "idleTimeout": 3600
    }
}

# Mock invalid response (e.g., 400 Bad Request)
mock_invalid_response = {
    "status": 400,
    "message": "Bad Request",
    "data": None
}

# Mock no response (None)
mock_no_response = None

@pytest.mark.asyncio
async def test_get_organization_basic_settings():
    # Mock the 'get' method of AsyncAPIClient to return the mock valid response
    mock_get = AsyncMock(return_value=mock_org_settings_data)

    # Create an instance of AsyncAPIClient with the mock get method
    client = AsyncAPIClient(
        base_url="https://api.example.com",
        auth=DummyAuthenticator()
    )
    client.get = mock_get  # Mocking the actual API call

    # Define the organization ID
    org_id = "123"

    # Run the method
    response: Optional[ApiResponse[Organization]] = await client.getOrganizationBasicSettings(org_id)

    # Assertions for valid response
    assert response is not None
    assert response.status == 200
    assert response.data.id == org_id
    assert response.data.name == "ALE"
    assert response.data.enforceStrongPassword is True
    assert response.data.timezone == "Europe/Tirane"
    assert response.data.auditHour == 130
    assert response.data.idleTimeout == 3600

    # Close the client after the test
    await client.close()


@pytest.mark.asyncio
async def test_get_organization_invalid_status():
    # Mock the 'get' method of AsyncAPIClient to return the mock invalid response
    mock_get = AsyncMock(return_value=mock_invalid_response)

    # Create an instance of AsyncAPIClient with the mock get method
    client = AsyncAPIClient(
        base_url="https://api.example.com",
        auth=DummyAuthenticator()
    )
    client.get = mock_get  # Mocking the actual API call

    # Define the organization ID
    org_id = "123"

    # Run the method
    response: Optional[ApiResponse[Organization]] = await client.getOrganizationBasicSettings(org_id)

    # Assertions for invalid response
    assert response is not None
    assert response.status == 400
    assert response.message == "Bad Request"
    assert response.data is None

    # Close the client after the test
    await client.close()


@pytest.mark.asyncio
async def test_get_organization_no_response():
    # Mock the 'get' method of AsyncAPIClient to return None (no response)
    mock_get = AsyncMock(return_value=mock_no_response)

    # Create an instance of AsyncAPIClient with the mock get method
    client = AsyncAPIClient(
        base_url="https://api.example.com",
        auth=DummyAuthenticator()
    )
    client.get = mock_get  # Mocking the actual API call

    # Define the organization ID
    org_id = "123"

    # Run the method
    response: Optional[ApiResponse[Organization]] = await client.getOrganizationBasicSettings(org_id)

    # Assertions for no response
    assert response is None

    # Close the client after the test
    await client.close()
