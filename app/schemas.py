from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class Medication(BaseModel):
    medicationName: str
    description: str
    usedFor: str
    dontTakeWith: list[str]
