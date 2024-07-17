from .handler import Handler
from ..models.service import Service
from pymongo.collection import Collection
from typing import Dict, Any, List
from ..utils.type import Type
from datetime import datetime

class ServiceHandler(Handler):
    def insert(self, services: List[Service], collection: Collection) -> List[int]:
        if not all(isinstance(service, Service) for service in services):
            raise ValueError(f"Input data expected to be a list of Service objects.")
        
        services_data = []
        for service in services:
            data = {
                "type": Type.SERVICE.value,
                "createdAt": datetime.today,
            }
            data.update(service.model_dump(by_alias=True))
            services_data.append(data)
        return collection.insert_many(services_data).inserted_ids
    
    def find(self, filter: Dict[str, Any], collection: Collection, max_docs: int = 5) -> List[Service]:
        if not isinstance(filter, dict):
            raise ValueError(f"Input data expected to be a dictionary")
        
        cursor = collection.find(filter).limit(max_docs)
        services = []

        for doc in cursor:
            service = Service(
                church_id = doc["churchId"],
                title = doc["title"],
                date_of_week = doc["dateOfWeek"],
                time = doc["time"]
            )
            services.append(service)
        cursor.close()

        if len(services) >= 1:
            return services
        return None