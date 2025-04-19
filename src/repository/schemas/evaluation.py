from pydantic import BaseModel, Field, ConfigDict


class Eval(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    anketa_id: int
    lover_id: int
    evaluation: bool


class EvalCreate(BaseModel):
    anketa_id: int = Field(...)
    lover_id: int = Field(...)
    evaluation: bool = Field(...)
