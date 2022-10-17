from pydantic import BaseModel, validator
from typing import Optional


class Country(BaseModel):
    name: Optional[str] = None

    @validator("*", pre=True, always=True)
    def check_for_none(cls, v):
        if v is None:
            raise ValueError("empty")
        return v


class Network(BaseModel):
    name: Optional[str] = None
    country: Optional[Country] = None

    @validator("*", pre=True, always=True)
    def check_for_none(cls, v):
        if v is None:
            raise ValueError("empty")
        return v


class TVProgram(BaseModel):
    name: Optional[str] = None
    network: Optional[Network] = None
    summary: Optional[str] = None

    @validator("*", pre=True, always=True)
    def check_for_none(cls, v):
        if v is None:
            raise ValueError("empty")
        return v
