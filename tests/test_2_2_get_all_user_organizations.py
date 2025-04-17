import pytest
import httpx
from httpx import Response, Request
from api_client.async_client import OVCirrusApiClient
from models.organization import Organization
from models.generic import ApiResponse
from api_client.auth import Authenticator

from typing import Optional
from datetime import datetime

# Dummy Authenticator that always returns a token
class DummyAuthenticator(Authenticator):
    def get_token(self) -> str:
        return "dummy-token"

    def force_relogin(self) -> bool:
        return True

# Mock response data for multiple organizations
mock_org_data = {
    "status": 200,
    "message": "Success",
    "data": [
        {
            "id": "123",
            "name": "ALE",
            "createdAt": "2022-08-04T12:10:38.058Z",
            "updatedAt": "2022-09-08T15:56:53.407Z",
            "enforceStrongPassword": True,
            "enforceStrongPasswordNotifyType": "SHOW_MESSAGE_AFTER_LOGIN"
        },
        {
            "id": "456",
            "name": "Another Org",
            "createdAt": "2022-01-01T10:00:00.000Z",
            "updatedAt": "2022-02-01T12:00:00.000Z",
            "enforceStrongPassword": False,
            "enforceStrongPasswordNotifyType": "NONE"
        }
    ]
}

@pytest.mark.asyncio
async def test_get_all_user_organizations():
    # Use MockTransport to intercept HTTPX requests
    async def mock_send(request: Request) -> Response:
        return Response(
            status_code=200,
            json=mock_org_data
        )

    transport = httpx.MockTransport(mock_send)

    # Inject httpx.AsyncClient with mock transport
    client = OVCirrusApiClient(
        base_url="https://api.example.com",
        auth=DummyAuthenticator()
    )
    client.client = httpx.AsyncClient(transport=transport)

    # Run the method
    response: Optional[ApiResponse[list[Organization]]] = await client.getAllUserOrganizations()

    # Assertions
    assert response is not None
    assert response.status == 200
    assert isinstance(response.data, list)
    assert len(response.data) == 2

    first_org = response.data[0]
    assert first_org.name == "ALE"
    assert first_org.enforceStrongPassword is True

    second_org = response.data[1]
    assert second_org.name == "Another Org"
    assert second_org.enforceStrongPassword is False

    await client.close()
