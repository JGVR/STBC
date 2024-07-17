from .handler import Handler
from ..models.church import Church
from pymongo.collection import Collection
from typing import Dict
from ..utils.type import Type
from datetime import datetime

class ChurchHandler(Handler):
    def insert(self, church: Church, collection: Collection) -> Dict[str, int]:
        if not isinstance(church, Church):
            raise ValueError(f"Input data expected to be a Church object.")
        
        data = {
            "type": Type.CHURCH.value,
            "createdAt": datetime.today
        }
        data.update(church.model_dump(by_alias=True))
        return {"_id": collection.insert_one(data).inserted_id}