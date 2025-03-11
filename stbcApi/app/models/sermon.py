from pydantic import BaseModel, Field, ConfigDict
from topic import Topic
from datetime import datetime
from typing import List

class Service(BaseModel):
    # > makes fields immutable after instantiation
    # > instantiation can be made by using property name or alias name
    # > strips white spaces from all str fields
    # > forbids any new properties from been added to the object upon instantiation
    model_config = ConfigDict(frozen=True, populate_by_name=True, str_strip_whitespace=True, extra='forbid')

    title: str = Field(max_length=300)
    url: str
    speaker_id: int = Field(gt=0, alias="speakerId")
    date: datetime
    topics: List[Topic]