from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class Member(BaseModel):
    # > makes fields immutable after instantiation
    # > instantiation can be made by using property name or alias name
    # > strips white spaces from all str fields
    # > forbids any new properties from been added to the object upon instantiation
    model_config = ConfigDict(frozen=True, populate_by_name=True, str_strip_whitespace=True, extra='forbid')

    church_id: int = Field(gt=0, alias="churchId")
    member_id: int = Field(gt=0, alias="memberId")
    first_name: str = Field(max_length=150, alias="firstName")
    middle_name: str = Field(max_length=150, default="", alias="middleName")
    last_name: str = Field(max_length=150, alias="lastName")
    title: str = Field(max_length=100, default="")
    short_bio: str = Field(max_length=500, default="", alias="shortBio")
    email_address: str = Field(default="", alias="emailAddress")
    phone_number: str = Field(default="", alias="phoneNumber")
    image_url: str = Field(default="", alias="imageUrl")
    start_date: datetime = Field(default="", alias="startDate")
    end_date: datetime = Field(default="", alias="endDate")