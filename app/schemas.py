from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class Medication(BaseModel):
    name: str
    description: str
    usedFor: str
    dontTakeWith: list[str]
    user_id: int


class MedicationOut(Medication):
    name: str
    description: str
    used_For: str
    dont_take_with: list[str]


class User(BaseModel):
    email: str
    password: str


class TokenData(BaseModel):
    id: Optional[str] = None
