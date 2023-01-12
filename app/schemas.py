from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class Medication(BaseModel):
    medicationName: str
    description: str
    usedFor: str
    dontTakeWith: list[str]


class MedicationOut(Medication):
    medication: str
    description: str
    used_For: str
    dont_take_with: list[str]
