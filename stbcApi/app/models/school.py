from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from ..utils.week_days import WeekDays
from .church_class import Class
from typing import List

class School(BaseModel):
    # > makes fields immutable after instantiation
    # > instantiation can be made by using property name or alias name
    # > strips white spaces from all str fields
    # > forbids any new properties from been added to the object upon instantiation
    model_config = ConfigDict(frozen=True, populate_by_name=True, str_strip_whitespace=True, extra='forbid')

    church_id: int = Field(gt=0, alias="churchId")
    school_id: int = Field(gt=0, alias="schoolId")
    name: str = Field(max_length=150)
    short_description: str = Field(max_length=500, alias="shortDescription")
    description: str = Field(default="")
    date_of_week: WeekDays | str
    time: datetime
    image_url: str = Field(default="", alias="imageUrl")
    classes: List[Class]