from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class Location(BaseModel):
    type: Optional[str] = "Point"
    coordinates: Optional[List[str]] = Field(default_factory=list)


class Site(BaseModel):
    id: Optional[str] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    name: Optional[str] = None
    countryCode: Optional[str] = None
    timezone: Optional[str] = None
    address: Optional[str] = None
    location: Optional[Location] = None
    imageUrl: Optional[str] = ""
    isDefault: Optional[bool] = False
    zoom: Optional[int] = 18
    organization: Optional[str] = None
