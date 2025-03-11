from .handler import Handler
from ..models.ministry import Ministry
from pymongo.collection import Collection
from typing import Dict, Any, List
from ..utils.type import Type
from datetime import datetime
from bson import ObjectId

class MinistryHandler(Handler):
    def insert(self, ministries: List[Ministry], collection: Collection) -> List[str]:
        if not all(isinstance(ministry, Ministry) for ministry in ministries):
            raise ValueError(f"Input data expected to be a list of Ministry objects.")
        
        ministries_data = []
        last_doc = collection.find_one(filter={"type": "ministry"}, sort=[("recordId", -1)])
        last_id = last_doc["recordId"] if last_doc else 0
        for ministry in ministries:
            last_id+=1
            data = {
                "_id":ObjectId(), 
                "type": Type.MINISTRY.value,
                "createdAt": datetime.now(),
                "recordId": last_id
            }
            data.update(ministry.model_dump(by_alias=True, exclude={"id"}))
            ministries_data.append(data)
        return [str(id) for id in collection.insert_many(ministries_data).inserted_ids]
    
    def find(self, filter: Dict[str, Any], collection: Collection, max_docs: int = 5) -> List[Ministry]:
        if not isinstance(filter, dict):
            raise ValueError(f"Input data expected to be a dictionary")
        recordId = filter.pop("recordId",0)

        cursor = collection.find({
            **filter,
            "recordId": {"$gt": recordId}
        }, sort=[("recordId", 1)]).limit(max_docs)
        ministries = []

        for doc in cursor:
            ministry = Ministry(
                id = int(doc["recordId"]),
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