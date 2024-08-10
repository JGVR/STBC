from abc import ABC, abstractmethod
from typing import Dict, Any
from pymongo.collection import Collection

class Handler(ABC):
    @abstractmethod
    def insert() -> None:
        pass

    @abstractmethod
    def find() -> None:
        pass

    def update(self, filter: Dict[str, Any], new_data: Dict[str, Any], collection: Collection) -> Dict[str, int]:
        if not isinstance(filter, dict) or not isinstance(new_data, dict):
            raise ValueError(f"The filter and new data input parameters must be a dictionary")
        result = collection.update_one(filter, {"$set": new_data})
        return {"count": result.modified_count}

    def delete(self, filter: Dict[str, Any], collection: Collection) -> Dict[str, int]:
        if not isinstance(filter, dict):
            raise ValueError(f"The filter input parameter must be a dictionary")
        
        return {"count": collection.delete_one(filter).deleted_count}