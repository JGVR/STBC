from .handler import Handler
from ..models.devotion import Devotion
from pymongo.collection import Collection
from typing import Dict, Any, List
from ..utils.type import Type
from datetime import datetime
from bson import ObjectId

class DevotionHandler(Handler):
    def insert(self, devotion: Devotion, collection: Collection) -> Dict[str, str]:
        if not isinstance(devotion, Devotion):
            raise ValueError(f"Input data expected to be a Devotion object.")
        
        data = {
            "_id": ObjectId(),
            "type": Type.DEVOTION.value,
            "createdAt": datetime.now()
        }
        data.update(devotion.model_dump(by_alias=True))
        return {"_id": str(collection.insert_one(data).inserted_id)}
    
    def find(self, filter: Dict[str, Any], collection: Collection, max_docs: int = 5) -> List[Devotion]:
        if not isinstance(filter, dict):
            raise ValueError(f"Input data expected to be a dictionary")
        
        cursor = collection.find(filter).limit(max_docs)
        devotions = []

        for doc in cursor:
            devotion = Devotion(
                church_id = doc["churchId"],
                member_id = doc["memberId"],
                title = doc["title"],
                week_day = doc["weekDay"],
                message = doc["message"]
            )
            devotions.append(devotion)
        cursor.close()

        if len(devotions) >= 1:
            return devotions
        return None