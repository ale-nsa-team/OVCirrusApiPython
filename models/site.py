from typing import List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime


class Coordinates(BaseModel):
    type: Optional[str] = Field(default=None)
    coordinates: Optional[Union[List[float], List[List[float]], List[List[List[float]]]]] = Field(default=None)


class Floor(BaseModel):
    createdAt: Optional[datetime] = Field(default=None)
    updatedAt: Optional[datetime] = Field(default=None)
    id: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    floorNumber: Optional[int] = Field(default=0)
    floorPlanUrl: Optional[str] = Field(default=None)
    floorPlanImageCoordinates: Optional[Coordinates] = Field(default=None)
    relativeAltitude: Optional[int] = Field(default=0)
    areaGeometry: Optional[Coordinates] = Field(default=None)
    area: Optional[float] = Field(default=0)
    areaUnit: Optional[str] = Field(default=None)
    building: Optional[str] = Field(default=None)
    site: Optional[str] = Field(default=None)
    organization: Optional[str] = Field(default=None)


class Building(BaseModel):
    createdAt: Optional[datetime] = Field(default=None)
    updatedAt: Optional[datetime] = Field(default=None)
    id: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    site: Optional[str] = Field(default=None)
    organization: Optional[str] = Field(default=None)
    floors: Optional[List[Floor]] = Field(default_factory=list)


class Location(BaseModel):
    type: Optional[str] = Field(default=None)
    coordinates: Optional[List[str]] = Field(default_factory=list)


class Site(BaseModel):
    id: Optional[str] = Field(default=None)
    createdAt: Optional[datetime] = Field(default=None)
    updatedAt: Optional[datetime] = Field(default=None)
    name: Optional[str] = Field(default=None)
    countryCode: Optional[str] = Field(default=None)
    timezone: Optional[str] = Field(default=None)
    address: Optional[str] = Field(default=None)
    location: Optional[Location] = Field(default=None)
    imageUrl: Optional[str] = Field(default="")
    isDefault: Optional[bool] = Field(default=False)
    zoom: Optional[int] = Field(default=18)
    organization: Optional[str] = Field(default=None)
    buildings: Optional[List[Building]] = Field(default_factory=list)
