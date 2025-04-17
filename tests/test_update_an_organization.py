import pytest
import httpx
from httpx import Response, Request
from typing import Optional
from api_client.async_client import OVCirrusApiClient
from api_client.auth import Authenticator
from models.organization import Organization
from models.generic import ApiResponse
from pydantic import ValidationError

# Dummy authenticator for tests
class DummyAuthenticator(Authenticator):
    def get_token(self) -> str:
        return "dummy-token"
    def force_relogin(self) -> bool:
        return False

# Sample payload for a valid organization
valid_org = Organization(
    id="123",
    name="ALE",
    enforceStrongPassword=True,
    enforceStrongPasswordNotifyType="SHOW_MESSAGE_AFTER_LOGIN",
    timezone="Europe/Tirane",
    auditHour=130,
    idleTimeout=3600
)

# Mock successful response
mock_success_response = {
    "status": 200,
    "message": "Updated successfully",
    "data": {
        "id": "123",
        "name": "ALE",
        "enforceStrongPassword": True,
        "enforceStrongPasswordNotifyType": "SHOW_MESSAGE_AFTER_LOGIN",
        "timezone": "Europe/Tirane",
        "auditHour": 130,
        "idleTimeout": 3600
    }
}

# Mock error response
mock_error_response = {
    "status": 400,
    "message": "Invalid data",
    "data": {}
}

# Mock malformed response
mock_malformed_response = {
    "status": 200,
    "message": "Missing data key",
    'data': {
        "sss" : "sss"
    }
}

@pytest.mark.asyncio
async def test_update_organization_success():
    async def mock_send(request: Request) -> Response:
        return Response(200, json=mock_success_response)

    transport = httpx.MockTransport(mock_send)
    client = OVCirrusApiClient("https://api.example.com", DummyAuthenticator())
    client.client = httpx.AsyncClient(transport=transport)

    response: Optional[ApiResponse[Organization]] = await client.updateOrganization("123", valid_org)

    assert response is not None
    assert response.status == 200
    assert response.data.id == "123"
    assert response.data.name == "ALE"

    await client.close()

@pytest.mark.asyncio
async def test_update_organization_invalid_data():
    async def mock_send(request: Request) -> Response:
        return Response(400, json=mock_error_response)

    transport = httpx.MockTransport(mock_send)
    client = OVCirrusApiClient("https://api.example.com", DummyAuthenticator())
    client.client = httpx.AsyncClient(transport=transport)

    response = await client.updateOrganization("123", valid_org)

    assert response is not None
    assert response.status == 400
    assert response.message == "Invalid data"
    assert isinstance(response.data, Organization)

    await client.close()

@pytest.mark.asyncio
async def test_update_organization_no_response():
    async def mock_send(request: Request) -> Response:
        return Response(204)  # No content

    transport = httpx.MockTransport(mock_send)
    client = OVCirrusApiClient("https://api.example.com", DummyAuthenticator())
    client.client = httpx.AsyncClient(transport=transport)

    response = await client.updateOrganization("123", valid_org)

    assert response is None
    await client.close()

# @pytest.mark.asyncio
# async def test_update_organization_malformed_response():
#     async def mock_send(request: Request) -> Response:
#         return Response(200, json=mock_malformed_response)

#     transport = httpx.MockTransport(mock_send)
#     client = OVCirrusApiClient("https://api.example.com", DummyAuthenticator())
#     client.client = httpx.AsyncClient(transport=transport)

#     with pytest.raises(ValidationError):  # You can catch a more specific one depending on your validation
#         await client.updateOrganization("123", valid_org)

#     await client.close()
