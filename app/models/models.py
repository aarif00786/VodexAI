from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class Item(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    quantity: Optional[int] = None
    inserted_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None

class Record(BaseModel):
    email: Optional[str] = None
    inserted_date: Optional[datetime] = None
    location : Optional[str] = None
