from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class Medication(BaseModel):
    medicationName: str
    description: str
    usedFor: str
    dontTakeWith: list[str]


class MedicationOut(Medication):
    pass


class User(BaseModel):
    email: str
    password: str


class TokenData(BaseModel):
    id: Optional[str] = None
