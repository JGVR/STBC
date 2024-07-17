from .handler import Handler
from ..models.ministry import Ministry
from pymongo.collection import Collection
from typing import Dict, Any, List
from ..utils.type import Type
from datetime import datetime

class MinistryHandler(Handler):
    def insert(self, ministries: List[Ministry], collection: Collection) -> List[int]:
        if not all(isinstance(ministry, Ministry) for ministry in ministries):
            raise ValueError(f"Input data expected to be a list of Ministry objects.")
        
        ministries_data = []
        for ministry in ministries:
            data = {
                "type": Type.MINISTRY.value,
                "createdAt": datetime.today,
            }
            data.update(ministry.model_dump(by_alias=True))
            ministries_data.append(data)
        return collection.insert_many(ministries_data).inserted_ids
    
    def find(self, filter: Dict[str, Any], collection: Collection, max_docs: int = 5) -> List[Ministry]:
        if not isinstance(filter, dict):
            raise ValueError(f"Input data expected to be a dictionary")
        
        cursor = collection.find(filter).limit(max_docs)
        ministries = []

        for doc in cursor:
            ministry = Ministry(
                church_id = doc["churchId"],
                name = doc["name"],
                description = doc["description"],
                image_url = doc["imageUrl"],
                register_url = doc["registerUrl"]
            )
            ministries.append(ministry)
        cursor.close()

        if len(ministries) >= 1:
            return ministries
        return None