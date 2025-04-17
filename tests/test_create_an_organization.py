import pytest
from unittest.mock import AsyncMock
from api_client.async_client import OVCirrusApiClient
from models.organization import Organization
from models.generic import ApiResponse
from datetime import datetime, timezone

@pytest.mark.asyncio
async def test_create_an_organization():
    # Create an example organization instance
    org = Organization(
        id="62d65f2506af3feef8fec051",
        name="ALE",
        createdAt=datetime.now(timezone.utc),
        updatedAt=datetime.now(timezone.utc),
        is2FARequired=False,
        imageUrl="",
        countryCode="FR",
        timezone="Europe/Tirane",
        auditHour=130,
        idleTimeout=3600,
        msp="60c8bce3eb5b4155f8b82214",
        upamAuthRecords=30,
        events=30,
        alerts=30,
        wifiRtls=30,
        networkAnalytics=30,
        clientSessions=30,
        clientAnalytics=30,
        auditLogs=7,
        loginAttemps=7,
        iotData=7,
        backupPerDevice=30,
        collectInfo=7,
        configurationBackup=5,
        qoe=30,
        enforceStrongPassword=True,
        enforceStrongPasswordNotifyType="SHOW_MESSAGE_AFTER_LOGIN"
    )

    # Mocked API response (as a dict)
    fake_response = {
        "status": 200,
        "message": "The organization has been successfully fetched.",
        "data": org.model_dump()
    }

    # Create the client and mock `post`
    client = OVCirrusApiClient(base_url="http://mock.api", auth=AsyncMock())
    client.post = AsyncMock(return_value=fake_response)

    # Call the method
    response = await client.createAnOrganization(org)

    # Assertions
    assert response is not None
    assert isinstance(response, ApiResponse)
    assert response.status == 200
    assert response.data.name == "ALE"
    assert response.data.enforceStrongPassword is True
