from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class Devotion(BaseModel):
    # > makes fields immutable after instantiation
    # > instantiation can be made by using property name or alias name
    # > strips white spaces from all str fields
    # > forbids any new properties from been added to the object upon instantiation
    model_config = ConfigDict(frozen=True, populate_by_name=True, str_strip_whitespace=True, extra='forbid')

    church_id: int = Field(gt=0, alias="churchId")
    member_id: int = Field(gt=0, alias="memberId")
    devotion_id: int = Field(gt=0, alias="devotionId")
    title: str = Field(max_length=300)
    date: datetime = Field(default=datetime.today)
    message: str