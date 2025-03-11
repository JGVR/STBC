from pydantic import BaseModel, Field, ConfigDict
from typing import List

class Topic(BaseModel):
    # > makes fields immutable after instantiation
    # > instantiation can be made by using property name or alias name
    # > strips white spaces from all str fields
    # > forbids any new properties from been added to the object upon instantiation
    model_config = ConfigDict(frozen=True, populate_by_name=True, str_strip_whitespace=True, extra='forbid')

    topics: List[str]