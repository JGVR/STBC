from .handler import Handler
from ..models.church import Church
from pymongo.collection import Collection
from typing import Dict, Any
from ..utils.type import Type
from datetime import datetime
from bson import ObjectId

class ChurchHandler(Handler):
    def insert(self, church: Church, collection: Collection) -> Dict[str, int]:
        if not isinstance(church, Church):
            raise ValueError(f"Input data expected to be a Church object.")
        
        data = {
            "_id": ObjectId(),
            "type": Type.CHURCH.value,
            "createdAt": datetime.now()
        }
        data.update(church.model_dump(by_alias=True))
        return {"_id": collection.insert_one(data).inserted_id}
    
    def find(self, filter: Dict[str, Any], collection: Collection) -> Church:
        if not isinstance(filter, dict):
            raise ValueError(f"Input data expected to be a dictionary")
        
        data = collection.find_one(filter)
        if data is not None:
            return Church(
                church_id = data["churchId"],
                name = data["name"]
            )
        return None