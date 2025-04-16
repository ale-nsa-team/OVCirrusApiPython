from pydantic import BaseModel  # Use BaseModel directly
from typing import Optional, TypeVar, Generic  # Make sure to import the correct types

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):  # Inherit directly from BaseModel
    status: Optional[int] = None
    message: Optional[str] = None
    data: Optional[T] = None

