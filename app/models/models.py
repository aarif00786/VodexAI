from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime, date

class Item(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    quantity: Optional[int] = None
    inserted_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None

class Record(BaseModel):
    email: Optional[EmailStr] = None
    inserted_date: Optional[datetime] = None
    location : Optional[str] = None
