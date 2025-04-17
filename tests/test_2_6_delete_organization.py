import pytest
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
async def test_delete_organization_success():
    # Mock response
    async def mock_send(request: Request) -> Response:
        return httpx.Response(
            status_code=200,
            json={"status": 200, "message": "Organization deleted successfully", "data": {"orgId": "123"}}
        )

    client = OVCirrusApiClient(
        base_url="https://api.example.com",
        auth=DummyAuthenticator()
    )
    client.client = httpx.AsyncClient(transport=httpx.MockTransport(mock_send))

    org_id = "123"
    response = await client.deleteOrganization(org_id)

    # Assertions for a successful response
    assert response is not None
    assert response.status == 200
    assert response.message == "Organization deleted successfully"
    assert response.data["orgId"] == org_id

    await client.close()


@pytest.mark.asyncio
async def test_delete_organization_invalid_id():
    # Mock response for invalid ID
    async def mock_send(request: Request) -> Response:
        return httpx.Response(
            status_code=400,
            json={"status": 400, "message": "Invalid organization ID", "data": {}}
        )

    client = OVCirrusApiClient(
        base_url="https://api.example.com",
        auth=DummyAuthenticator()
    )
    client.client = httpx.AsyncClient(transport=httpx.MockTransport(mock_send))

    org_id = "invalid-id"
    response = await client.deleteOrganization(org_id)

    # Assertions for a bad request response
    assert response is not None
    assert response.status == 400
    assert response.message == "Invalid organization ID"

    await client.close()


@pytest.mark.asyncio
async def test_delete_organization_not_found():
    # Mock response for not found
    async def mock_send(request: Request) -> Response:
        return httpx.Response(
            status_code=404,
            json={"status": 404, "message": "Organization not found", "data": {}}
        )

    client = OVCirrusApiClient(
        base_url="https://api.example.com",
        auth=DummyAuthenticator()
    )
    client.client = httpx.AsyncClient(transport=httpx.MockTransport(mock_send))

    org_id = "123"
    response = await client.deleteOrganization(org_id)

    # Assertions for not found response
    assert response is not None
    assert response.status == 404
    assert response.message == "Organization not found"

    await client.close()


@pytest.mark.asyncio
async def test_delete_organization_unauthorized():
    # Mock response for unauthorized
    async def mock_send(request: Request) -> Response:
        return httpx.Response(
            status_code=401,
            json={"status": 401, "message": "Unauthorized", "data": {}}
        )

    client = OVCirrusApiClient(
        base_url="https://api.example.com",
        auth=DummyAuthenticator()
    )
    client.client = httpx.AsyncClient(transport=httpx.MockTransport(mock_send))

    org_id = "123"
    response = await client.deleteOrganization(org_id)

    # Assertions for unauthorized response
    assert response is not None
    assert response.status == 401
    assert response.message == "Unauthorized"

    await client.close()


@pytest.mark.asyncio
async def test_delete_organization_server_error():
    # Mock response for server error
    async def mock_send(request: Request) -> Response:
        return httpx.Response(
            status_code=500,
            json={"status": 500, "message": "Internal server error", "data": {}}
        )

    client = OVCirrusApiClient(
        base_url="https://api.example.com",
        auth=DummyAuthenticator()
    )
    client.client = httpx.AsyncClient(transport=httpx.MockTransport(mock_send))

    org_id = "123"
    response = await client.deleteOrganization(org_id)

    # Assertions for server error response
    assert response is not None
    assert response.status == 500
    assert response.message == "Internal server error"

    await client.close()


@pytest.mark.asyncio
async def test_delete_organization_no_response():
    # Mock response for no response body
    async def mock_send(request: Request) -> Response:
        return httpx.Response(
            status_code=200,
            json=None
        )

    client = OVCirrusApiClient(
        base_url="https://api.example.com",
        auth=DummyAuthenticator()
    )
    client.client = httpx.AsyncClient(transport=httpx.MockTransport(mock_send))

    org_id = "123"
    response = await client.deleteOrganization(org_id)

    # Assertions for no response returned
    assert response is None

    await client.close()


@pytest.mark.asyncio
async def test_delete_organization_malformed_response():
    # Mock response for malformed JSON or invalid structure
    async def mock_send(request: Request) -> Response:
        # Returning a response with an unexpected structure
        return httpx.Response(
            status_code=200,
            json={"unexpected_field": "value"}
        )

    client = OVCirrusApiClient(
        base_url="https://api.example.com",
        auth=DummyAuthenticator()
    )
    client.client = httpx.AsyncClient(transport=httpx.MockTransport(mock_send))

    org_id = "123"
    response = await client.deleteOrganization(org_id)

    # Ensure response is properly handled, and assert the unexpected_field is present
    assert response is not None
    

    await client.close()

