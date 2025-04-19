from pydantic import BaseModel, Field, ConfigDict


class Relationship(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user1: int
    user2: int
    status: str


class RelationshipCreate(BaseModel):
    user1: int = Field(...)
    user2: int = Field(...)
    status: str = Field(...)
