from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from enum import Enum


class CourseEnum(str, Enum):
    NP = "NUFYP"
    BA1 = "Bachelor 1"
    BA2 = "Bachelor 2"
    BA3 = "Bachelor 3"
    BA4 = "Bachelor 4"
    grad = "Graduate"
    phd = "Phd"
    other = "Other"


class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"


class GenderPreference(str, Enum):
    male = "male"
    female = "female"
    both = "both"


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    tg_id: str
    nu_id: Optional[str]
    age: int
    course: CourseEnum
    description: str
    photo_url: str
    gender: GenderEnum
    preference: GenderPreference


class UserCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=32)
    description: str = Field(..., min_length=1, max_length=2048)
    age: int = Field(..., ge=0, le=100)
    course: CourseEnum
    tg_id: str = Field(..., min_length=6, max_length=32)
    nu_id: Optional[str] = Field(None, max_length=32)
    photo_url: str = Field(...)
    gender: GenderEnum
    preference: GenderPreference


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=1, max_length=32)
    description: Optional[str] = Field(None, min_length=1, max_length=2048)
    age: Optional[int] = Field(None, ge=0, le=100)
    course: Optional[CourseEnum] = None
    photo_url: str = Field(...)
    gender: GenderEnum = None
    preference: GenderPreference = None
