import pytest
import httpx
from httpx import Request, Response

from api_client.async_client import OVCirrusApiClient
from api_client.auth import Authenticator
from models.generic import ApiResponse
from models.user import UserProfile
from unittest.mock import patch
from typing import Optional
from utilities.model_validator import safe_model_validate

class DummyAuthenticator(Authenticator):
    def get_token(self) -> str:
        return "dummy-token"
    def force_relogin(self) -> bool:
        return True


# Mock success data
mock_user_profile_data = {
    "status": 200,
    "message": "OK",
    "data": {
        "id": "u-001",
        "firstname": "John Doe",
        "email": "john@example.com"
    }
}

@pytest.mark.asyncio
async def test_get_user_profile_success():
    async def mock_send(request: Request) -> Response:
        return Response(
            status_code=200,
            json=mock_user_profile_data
        )

    transport = httpx.MockTransport(mock_send)
    client = OVCirrusApiClient(
        base_url="https://api.example.com",
        auth=DummyAuthenticator()
    )
    client.client = httpx.AsyncClient(transport=transport)

    response = await client.getUserProfile()

    assert response is not None
    assert response.status == 200
    assert response.data.firstname == "John Doe"

    await client.close()

@pytest.mark.asyncio
async def test_get_user_profile_invalid_structure():
    async def mock_send(request: Request) -> Response:
        # This data should be missing required fields or have unexpected structure
        return Response(
            status_code=200,
            json={"status": 200, "message": "OK", "data": {"unexpected_field": "oops"}}
        )

    transport = httpx.MockTransport(mock_send)
    client = OVCirrusApiClient(
        base_url="https://api.example.com",
        auth=DummyAuthenticator()
    )
    client.client = httpx.AsyncClient(transport=transport)

    response = await client.getUserProfile()

    # Should fail validation and return None
    assert response is None

    await client.close()




@pytest.mark.asyncio
async def test_get_user_profile_no_response():
    async def mock_send(request: Request) -> Response:
        return Response(status_code=204)

    client = OVCirrusApiClient("https://api.example.com", auth=DummyAuthenticator())
    client.client = httpx.AsyncClient(transport=httpx.MockTransport(mock_send))

    result = await client.getUserProfile()
    assert result is None
    await client.close()


@pytest.mark.asyncio
async def test_get_user_profile_unauthorized():
    call_count = 0

    async def mock_send(request: Request) -> Response:
        nonlocal call_count
        call_count += 1
        return Response(
            status_code=401,
            json={"status": 401, "message": "Unauthorized"}
        )

    transport = httpx.MockTransport(mock_send)
    client = OVCirrusApiClient(
        base_url="https://api.example.com",
        auth=DummyAuthenticator()
    )
    client.client = httpx.AsyncClient(transport=transport)

    result = await client.getUserProfile()

    assert result is not None  # Because force_relogin() fails after retry
    assert call_count == 2  # First attempt + retry

    await client.close()

@pytest.mark.asyncio
async def test_get_user_profile_retry_success():
    call_count = 0

    async def mock_send(request: Request) -> Response:
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return Response(
                status_code=401,
                json={"status": 401, "message": "Unauthorized"}
            )
        return Response(
            status_code=200,
            json={
                "status": 200,
                "message": "OK",
                "data": {
                    "id": "u123",
                    "firstname": "Jane Doe",
                    "email": "jane@example.com",
                    "failedTry": 0
                }
            }
        )

    transport = httpx.MockTransport(mock_send)
    client = OVCirrusApiClient(
        base_url="https://api.example.com",
        auth=DummyAuthenticator()
    )
    client.client = httpx.AsyncClient(transport=transport)

    result = await client.getUserProfile()

    assert result is not None
    assert result.status == 200
    assert result.data.firstname == "Jane Doe"
    assert call_count == 2  # Retry happened

    await client.close()


@pytest.mark.asyncio
async def test_get_user_profile_malformed_json():
    # Simulating an invalid JSON response (single quotes instead of double quotes)
    invalid_json_response = "{'status': 200, 'message': 'OK', 'data': {'name': 'Jane Doe'}}"

    # Mock the logger used in the OVCirrusApiClient or wherever it's being called from
    with patch('api_client.async_client.logger') as mock_logger:
        mock_logger.reset_mock()  # Reset any previous calls

        # Simulate the validation process
        try:
            # This should raise an exception due to the malformed JSON
            result = safe_model_validate(ApiResponse[UserProfile], invalid_json_response)
        except Exception as e:
            # Check if the error is being caught
            print(f"Caught exception: {str(e)}")
        
        # Assert that the result is None due to invalid JSON
        assert result is None

        # Assert that the logger's error method was called with the correct error message
        mock_logger.error.assert_called_with(
            'Unexpected error during model validation for ApiResponse[UserProfile]: JSON Decode error'
        )

        # If no exception was raised in the above block, you can try a manual print to debug
        if not mock_logger.error.called:
            print("Error logging was not called, check the patch path and exception handling.")
