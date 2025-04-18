import pytest
from unittest.mock import AsyncMock, patch
from api_client.async_client import OVCirrusApiClient
from typing import Optional, Dict, List, Any

from models.site import Site
from models.generic import ApiResponse
from utilities.model_validator import safe_model_validate

@pytest.mark.asyncio
class TestGetOrganizationSites:

    @pytest.fixture
    def client(self):
        client = OVCirrusApiClient(base_url="https://api.example.com", auth=AsyncMock())
        client.get = AsyncMock()
        return client

    @pytest.fixture
    def org_id(self):
        return "org-abc123"

    @pytest.fixture
    def valid_response(self):
        return {
            "status": 200,
            "message": "Success",
            "data": [
                {
                    "id": "site-123",
                    "name": "Test Site",
                    "countryCode": "US",
                    "timezone": "America/New_York",
                    "address": "123 Main Street",
                    "location": {
                        "type": "Point",
                        "coordinates": ["-73.935242", "40.730610"]
                    },
                    "isDefault": False,
                    "zoom": 12,
                    "organization": "org-abc123"
                }
            ]
        }

    async def test_get_organization_sites_success(self, client, org_id, valid_response):
        client.get.return_value = valid_response
        result = await client.getOrganizationSites(org_id)

        assert result is not None
        assert isinstance(result, ApiResponse)
        assert isinstance(result.data, list)
        assert isinstance(result.data[0], Site)
        assert result.data[0].name == "Test Site"

    async def test_get_organization_sites_no_response(self, client, org_id):
        client.get.return_value = None
        result = await client.getOrganizationSites(org_id)

        assert result is None

    async def test_get_organization_sites_invalid_data(self, client, org_id):
        client.get.return_value = {
            "status": 200,
            "message": "Success",
            "data": [{"name": 123}]
        }

        result = await client.getOrganizationSites(org_id)
        assert result is None

    async def test_get_organization_sites_invalid_structure(self, client, org_id):
        malformed_data = "{'status': 200, 'message': 'OK', 'data': {'invalid_field': 'xyz'}}"  # Not a dict
        with patch("utilities.model_validator.logger") as mock_logger:
            client.get.return_value = {"unexpected": "structure"}
            result = safe_model_validate(ApiResponse[Site], malformed_data)

          # safe_model_validate should return None on failure
            assert result is None

            # Ensure a warning was logged
            assert mock_logger.warning.called
            args, _ = mock_logger.warning.call_args
            assert "Validation failed for ApiResponse[Site]" in args[0]  

    async def test_get_organization_sites_malformed_json(self, client, org_id):
        malformed_data = "{'status': 200, 'message': 'OK', 'data': {'name': 'Jane Doe'}}"  # Not a dict
        with patch("utilities.model_validator.logger") as mock_logger:
            client.get.return_value = {"unexpected": "structure"}
            result = safe_model_validate(ApiResponse[Site], malformed_data)

          # safe_model_validate should return None on failure
            assert result is None

            # Ensure a warning was logged
            assert mock_logger.warning.called
            args, _ = mock_logger.warning.call_args
            assert "Validation failed for ApiResponse[Site]" in args[0]

    async def test_get_organization_sites_http_exception(self, client, org_id):
        client.get.side_effect = Exception("Internal Server Error")

        with pytest.raises(Exception):
            await client.getOrganizationSites(org_id)
