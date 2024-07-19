from typing import List, Dict, Union, Any
from ..models.church import Church
from ..models.devotion import Devotion
from ..models.event import Event
from ..models.member import Member
from ..models.ministry import Ministry
from ..models.school import School
from ..models.service import Service

class ModelIdentifier:
    @staticmethod
    def call(type: str, req_data: Dict[str, Any]) -> Union[Church, Devotion, Event, Member, Ministry, School, Service]:
        match type:
            case "church":
                return Church(**req_data)
            case "devotion":
                return Devotion(**req_data)
            case "event":
                return Event(**req_data)
            case "member":
                return Member(**req_data)
            case "ministry":
                return Ministry(**req_data)
            case "school":
                return School(**req_data)
            case _:
                return Service(**req_data)