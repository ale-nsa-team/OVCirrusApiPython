import pytest
import httpx
from httpx import Response, Request
from api_client.async_client import OVCirrusApiClient
from models.organization import Organization
from models.generic import ApiResponse
from api_client.auth import Authenticator

from typing import Optional
from datetime import datetime

from httpx import HTTPStatusError, Request, Response
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
class TestGetAllUserOrganizations:

    @pytest.fixture
    def client(self):
        client = OVCirrusApiClient(base_url="https://api.example.com", auth=AsyncMock())
        client.get = AsyncMock()
        return client

    @pytest.fixture
    def valid_response(self):
        return {
            "status": 200,
            "message": "Fetched organizations",
            "data": [
                {
                    "id": "123",
                    "name": "Org One",
                    "timezone": "Europe/Paris"
                },
                {
                    "id": "456",
                    "name": "Org Two",
                    "timezone": "Asia/Tokyo"
                }
            ]
        }

    async def test_get_all_user_organizations_success(self, client, valid_response):
        client.get.return_value = valid_response
        response = await client.getAllUserOrganizations()
        assert response is not None
        # assert response.status == 200
        # assert len(response.data) == 2
        # assert response.data[0].name == "Org One"

    async def test_get_all_user_organizations_no_response(self, client):
        client.get.return_value = None
        response = await client.getAllUserOrganizations()
        assert response is None

    async def test_get_all_user_organizations_invalid_structure(self, client):
        client.get.return_value = {
            "status": 200,
            "message": "Invalid",
            "data": [
                {
                    "id": "123",
                    "name": 123,  # Invalid type
                    "timezone": True  # Invalid type
                }
            ]
        }
        response = await client.getAllUserOrganizations()
        assert response is None

    # async def test_get_all_user_organizations_http_error(self, client):
    #     mock_response = Response(
    #         status_code=500,
    #         request=Request("GET", "https://api.example.com/api/ov/v1/organizations"),
    #         content=b"Server Error"
    #     )
    #     client.get.side_effect = HTTPStatusError("Server error", request=mock_response.request, response=mock_response)

    #     with patch("OVCirrusApiClient.logger") as mock_logger:
    #         response = await client.getAllUserOrganizations()
    #         assert response is None
    #         mock_logger.warning.assert_called()

    # async def test_get_all_user_organizations_malformed_json(self, client):
    #     client.get.return_value = "{status: 200, message: 'Malformed'}"  # Not a valid dict

    #     with patch("utilities.model_validator.safe_model_validate", return_value=None):
    #         response = await client.getAllUserOrganizations()
    #         assert response is None
