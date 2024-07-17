from .handler import Handler
from ..models.event import Event
from pymongo.collection import Collection
from typing import Dict, Any, List
from ..utils.type import Type
from datetime import datetime

class EventHandler(Handler):
    def insert(self, events: List[Event], collection: Collection) -> List[int]:
        if not all(isinstance(event, Event) for event in events):
            raise ValueError(f"Input data expected to be a list of Event objects.")
        
        events_data = []
        for event in events:
            data = {
                "type": Type.EVENT.value,
                "createdAt": datetime.today,
            }
            data.update(event.model_dump(by_alias=True))
            events_data.append(data)
        return collection.insert_many(events).inserted_ids
    
    def find(self, filter: Dict[str, Any], collection: Collection, max_docs: int = 5) -> List[Event]:
        if not isinstance(filter, dict):
            raise ValueError(f"Input data expected to be a dictionary")
        
        cursor = collection.find(filter).limit(max_docs)
        events = []

        for doc in cursor:
            event = Event(
                church_id = doc["churchId"],
                title = doc["title"],
                description = doc["description"],
                date = doc["date"],
                image_url = doc["imageUrl"],
                location = doc["location"]
            )
            events.append(event)
        cursor.close()

        if len(events) >= 1:
            return events
        return None