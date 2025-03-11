from .handler import Handler
from ..models.event import Event
from pymongo.collection import Collection
from typing import Dict, Any, List
from ..utils.type import Type
from datetime import datetime
from bson import ObjectId

class EventHandler(Handler):
    def insert(self, events: List[Event], collection: Collection) -> List[str]:
        if not all(isinstance(event, Event) for event in events):
            raise ValueError(f"Input data expected to be a list of Event objects.")
        
        events_data = []
        last_doc = collection.find_one(filter={"type": "event"}, sort=[("recordId", -1)])
        last_id = last_doc["recordId"] if last_doc else 0
        for event in events:
            last_id+=1
            data = {
                "_id": ObjectId(),
                "type": Type.EVENT.value,
                "createdAt": datetime.now(),
                "recordId": last_id
            }
            data.update(event.model_dump(by_alias=True, exclude={"id"}))
            events_data.append(data)
        return [str(id) for id in collection.insert_many(events_data).inserted_ids]
    
    def find(self, filter: Dict[str, Any], collection: Collection, max_docs: int = 5) -> List[Event]:
        if not isinstance(filter, dict):
            raise ValueError(f"Input data expected to be a dictionary")
        recordId = filter.pop("recordId",0)
        
        cursor = collection.find({
            **filter,
            "recordId": {"$gt": recordId}
        }, sort=[("recordId", 1)]).limit(max_docs)
        events = []

        for doc in cursor:
            event = Event(
                id = doc["recordId"],
                church_id = doc["churchId"],
                title = doc["title"],
                description = doc["description"],
                start_date = doc["startDate"],
                end_date = doc["endDate"],
                event_url = doc["eventUrl"],
                image_url = doc["imageUrl"],
                location = doc["location"]
            )
            events.append(event)
        cursor.close()

        if len(events) >= 1:
            return events
        return None