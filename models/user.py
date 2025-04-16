from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserProfile(BaseModel):
    failedTry: Optional[int] = 0
    lockedUntilDate: Optional[int] = 0
    lastLoginDate: Optional[datetime] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    id: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    verified: Optional[bool] = None
    preferredLanguage: Optional[str] = None
    country: Optional[str] = None
    closestRegion: Optional[str] = None
    companyName: Optional[str] = None
    avatarLocation: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    zipCode: Optional[str] = None
    phoneNumber: Optional[str] = None
    isTwoFAEnabled: Optional[bool] = None
    faMethod: Optional[str] = None
    tempSecret: Optional[str] = None
    secret: Optional[str] = None
    enforcementPolicy: Optional[str] = None
    accessLevelRole: Optional[str] = None
    # msp: Optional[str] = None

