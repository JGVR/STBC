from .handler import Handler
from ..models.sermon import Sermon
from pymongo.collection import Collection
from typing import Dict, Any, List
from ..utils.type import Type
from datetime import datetime
from bson import ObjectId

class SermonHandler(Handler):
    def insert(self, sermons: List[Sermon], collection: Collection) -> List[str]:
        if not all(isinstance(sermon, Sermon) for sermon in sermons):
            raise ValueError(f"Input data expected to be a list of Sermon objects.")
        
        sermons_data = []
        for sermon in sermons:
            data = {
                "_id": ObjectId(),
                "type": Type.SERMON.value,
                "createdAt": datetime.now()
            }
            data.update(sermon.model_dump(by_alias=True, exclude={"id"}))
            sermons_data.append(data)
            print(sermons_data)
        return [str(id) for id in collection.insert_many(sermons_data).inserted_ids]
    
    def find(self, filter: Dict[str, Any], collection: Collection, max_docs: int = 5) -> List[Sermon]:
        if not isinstance(filter, dict):
            raise ValueError(f"Input data expected to be a dictionary")
        
        cursor = collection.find({
            **filter
        }).limit(max_docs)
        sermons = []

        for doc in cursor:
            sermon = Sermon(
                church_id = doc["churchId"],
                title = doc["title"],
                url = doc["url"],
                speaker_id = doc["speakerId"],
                date = doc["date"],
                topics = doc["topics"]
            )
            sermons.append(sermon)
        cursor.close()

        if len(sermons) >= 1:
            return sermons
        return None