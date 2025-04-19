import pytest
import httpx
from httpx import Request, Response
from unittest.mock import AsyncMock
from api_client.async_client import OVCirrusApiClient
from models.user import UserResponse, UserProfile
from models.generic import ApiResponse
from api_client.auth import Authenticator

class DummyAuthenticator(Authenticator):
    def get_token(self) -> str:
        return "dummy-token"
    def force_relogin(self) -> bool:
        return True

@pytest.mark.asyncio
async def test_update_user_profile_success():
    user_profile = UserProfile(firstname="John Doe", email="john@example.com")
    mock_response_data = {
        "status": 200,
        "message": "Success",
        "data": user_profile.model_dump()
    }

    async def mock_send(request: Request) -> Response:
        return Response(status_code=200, json=mock_response_data)

    transport = httpx.MockTransport(mock_send)
    client = OVCirrusApiClient(base_url="https://api.example.com", auth=DummyAuthenticator())
    client.client = httpx.AsyncClient(transport=transport)

    result = await client.updateUserProfile(user_profile)

    assert result is not None
    assert isinstance(result, UserResponse)
    assert result.status == 200
    assert isinstance(result.data, UserProfile)
    assert result.data.firstname == "John Doe"

    await client.close()

@pytest.mark.asyncio
async def test_update_user_profile_invalid_data():
    user_profile = UserProfile(firstname="Invalid", email="bad@example.com")

    mock_response_data = {
        "status": 400,
        "message": "Bad Request",
        "errors": [ 
                {

                    "type": "any.required",
                    "field": "Lastname",
                    "errorMsg": "Lastname is required"

                }
        ]
    }

    async def mock_send(request: Request) -> Response:
        return Response(status_code=400, json=mock_response_data)

    transport = httpx.MockTransport(mock_send)
    client = OVCirrusApiClient(base_url="https://api.example.com", auth=DummyAuthenticator())
    client.client = httpx.AsyncClient(transport=transport)

    result = await client.updateUserProfile(user_profile)

    assert isinstance(result, UserResponse)
    assert result.status == 400
    assert result.message == "Bad Request"
    assert result.errors[0].errorMsg == "Lastname is required"

    await client.close()

@pytest.mark.asyncio
async def test_update_user_profile_no_response():
    user_profile = UserProfile(firstname="Nobody", email="null@example.com")

    async def mock_send(request: Request) -> Response:
        return Response(status_code=204)

    transport = httpx.MockTransport(mock_send)
    client = OVCirrusApiClient(base_url="https://api.example.com", auth=DummyAuthenticator())
    client.client = httpx.AsyncClient(transport=transport)

    result = await client.updateUserProfile(user_profile)

    assert result is None

    await client.close()

@pytest.mark.asyncio
async def test_update_user_profile_retry_on_401():
    user_profile = UserProfile(firstname="Retry Guy", email="retry@example.com")

    responses = [401, 200]
    count = 0

    async def mock_send(request: Request) -> Response:
        nonlocal count
        status = responses[count]
        count += 1
        if status == 401:
            return Response(status_code=401, json={"message": "Unauthorized"})
        return Response(status_code=200, json={
            "status": 200,
            "message": "Success",
            "data": user_profile.model_dump()
        })

    transport = httpx.MockTransport(mock_send)
    client = OVCirrusApiClient(base_url="https://api.example.com", auth=DummyAuthenticator())
    client.client = httpx.AsyncClient(transport=transport)

    result = await client.updateUserProfile(user_profile)

    assert result.status == 200
    assert result.data.firstname == "Retry Guy"

    await client.close()


@pytest.mark.asyncio
async def test_update_user_profile_invalid_header():
    # Create an example organization instance
    user_profile = UserProfile(firstname="Retry Guy", email="retry@example.com")
    mock_response = {
        "errorCode": 406,
        "errorMsg": "The 'Content-Type' header is missing or invalid. You should use 'Content-Type: application/json'.",
        "errorDetailsCode": "invalid_header"
    }
    
    client = OVCirrusApiClient(base_url="http://mock.api", auth=AsyncMock())

    client.put = AsyncMock(return_value=mock_response)

    result = await client.updateUserProfile(user_profile)

    assert result is not None
    assert isinstance(result, UserResponse)
    assert result.errorCode == 406
    assert result.errorMsg == "The 'Content-Type' header is missing or invalid. You should use 'Content-Type: application/json'."
    assert result.errorDetailsCode == "invalid_header"


@pytest.mark.asyncio
async def test_update_user_profile_malformed_response(caplog):
    user_profile = UserProfile(firstname="Mal", email="malformed@example.com")

    async def mock_send(request: Request) -> Response:
        return Response(status_code=200, content=b"{not: valid json")

    transport = httpx.MockTransport(mock_send)
    client = OVCirrusApiClient(base_url="https://api.example.com", auth=DummyAuthenticator())
    client.client = httpx.AsyncClient(transport=transport)

    result = await client.updateUserProfile(user_profile)

    assert result is None
    assert "Failed to decode JSON" in caplog.text

    await client.close()
