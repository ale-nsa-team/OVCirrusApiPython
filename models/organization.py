from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Organization(BaseModel):
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    id: Optional[str] = None
    name: Optional[str] = ""
    is2FARequired: Optional[bool] = False
    imageUrl: Optional[str] = ""
    countryCode: Optional[str] = ""
    timezone: Optional[str] = ""
    auditHour: Optional[int] = 0
    idleTimeout: Optional[int] = 0
    msp: Optional[str] = None
    upamAuthRecords: Optional[int] = 0
    events: Optional[int] = 0
    alerts: Optional[int] = 0
    wifiRtls: Optional[int] = 0
    networkAnalytics: Optional[int] = 0
    clientSessions: Optional[int] = 0
    clientAnalytics: Optional[int] = 0
    auditLogs: Optional[int] = 0
    loginAttemps: Optional[int] = 0
    iotData: Optional[int] = 0
    backupPerDevice: Optional[int] = 0
    collectInfo: Optional[int] = 0
    configurationBackup: Optional[int] = 0
    qoe: Optional[int] = 0
    enforceStrongPassword: Optional[bool] = False
    enforceStrongPasswordNotifyType: Optional[str] = "SHOW_MESSAGE_AFTER_LOGIN"
