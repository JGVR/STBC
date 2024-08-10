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
    def call(type: str, req_data: Union[Dict[str, Any], List[dict]]) -> Any:
        match type:
            case "church":
                if isinstance(req_data, list):
                    return [Church(**data) for data in req_data]
                return Church(**req_data)
            case "devotion":
                if isinstance(req_data, list):
                    return [Devotion(**data) for data in req_data]
                return Devotion(**req_data)
            case "event":
                if isinstance(req_data, list):
                    return [Event(**data) for data in req_data]
                return Event(**req_data)
            case "member":
                if isinstance(req_data, list):
                    return [Member(**data) for data in req_data]
                return Member(**req_data)
            case "ministry":
                if isinstance(req_data, list):
                    return [Ministry(**data) for data in req_data]
                return Ministry(**req_data)
            case "school":
                if isinstance(req_data, list):
                    return [School(**data) for data in req_data]
                return School(**req_data)
            case _:
                if isinstance(req_data, list):
                    return [Service(**data) for data in req_data]
                return Service(**req_data)