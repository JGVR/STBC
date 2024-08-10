from pydantic import BaseModel, Field, ConfigDict
from typing import List

class Class(BaseModel):
    # > makes fields immutable after instantiation
    # > instantiation can be made by using property name or alias name
    # > strips white spaces from all str fields
    # > forbids any new properties from been added to the object upon instantiation
    model_config = ConfigDict(frozen=True, populate_by_name=True, str_strip_whitespace=True, extra='forbid')

    member_ids: List[int] = Field(alias="memberIds")
    name: str = Field(max_length=150)
    ages: str = Field(max_length=100)