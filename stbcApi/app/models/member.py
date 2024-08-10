from pydantic import BaseModel, Field, ConfigDict, field_validator
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
    title: str = Field(max_length=50, default="")
    short_bio: str = Field(max_length=500, default="", alias="shortBio")
    email_address: str | None = Field(default="", pattern=r"^[\w,-]+@[a-zA-Z].{2,}$", alias="emailAddress")
    phone_number: str | None = Field(default=None, pattern=r"[0-9]{3}-[0-9]{3}-[0-9]{4}", alias="phoneNumber")
    image_url: str = Field(default="", alias="imageUrl")
    start_date: datetime | None = Field(default=None, alias="startDate")
    end_date: datetime | None = Field(default=None, alias="endDate")