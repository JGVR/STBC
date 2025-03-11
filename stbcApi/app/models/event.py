from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class Event(BaseModel):
    # > makes fields immutable after instantiation
    # > instantiation can be made by using property name or alias name
    # > strips white spaces from all str fields
    # > forbids any new properties from been added to the object upon instantiation
    model_config = ConfigDict(frozen=True, populate_by_name=True, str_strip_whitespace=True, extra='forbid')

    id: int = Field(default=0, alias="recordId")
    church_id: int = Field(gt=0, alias="churchId")
    title: str = Field(max_length=300)
    description: str = Field(max_length=1500)
    start_date: datetime = Field(default=None, alias="startDate")
    end_date: datetime = Field(default=None, alias="endDate")
    event_url: str = Field(default="", alias="eventUrl")
    image_url: str = Field(default="", alias="imageUrl")
    location: str = Field(default="")
