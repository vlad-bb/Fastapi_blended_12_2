from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr, PastDate


class ContactSchema(BaseModel):
    name: str
    second_name: str
    email: EmailStr
    phone: str
    birthday: PastDate
    address: Optional[str] = None


class ContactResponceSchema(BaseModel):
    id: int
    name: str
    second_name: str
    email: EmailStr
    phone: str
    birthday: PastDate
    address: str | None
