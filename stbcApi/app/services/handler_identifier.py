from typing import List, Dict, Union
from .church_handler import ChurchHandler
from .devotion_handler import DevotionHandler
from .event_handler import EventHandler
from .member_handler import MemberHandler
from .ministry_handler import MinistryHandler
from .school_handler import SchoolHandler
from .service_handler import ServiceHandler

class HandlerIdentifier:
    @staticmethod
    def call(type: str) -> Union[ChurchHandler, DevotionHandler, EventHandler, MemberHandler, MinistryHandler, SchoolHandler, ServiceHandler]:
        match type:
            case "church":
                return ChurchHandler()
            case "devotion":
                return DevotionHandler()
            case "event":
                return EventHandler()
            case "member":
                return MemberHandler()
            case "ministry":
                return MinistryHandler()
            case "school":
                return SchoolHandler()
            case _:
                return ServiceHandler()