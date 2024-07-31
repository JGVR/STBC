from .handler import Handler
from ..models.school import School
from ..models.church_class import Class
from pymongo.collection import Collection
from typing import Dict, Any, List
from ..utils.type import Type
from datetime import datetime
from bson import ObjectId

class SchoolHandler(Handler):
    def insert(self, schools: List[School], collection: Collection) -> List[ObjectId]:
        if not all(isinstance(school, School) for school in schools):
            raise ValueError(f"Input data expected to be a list of School objects.")
        
        schools_data = []
        for school in schools:
            data = {
                "_id": ObjectId(),
                "type": Type.SCHOOL.value,
                "createdAt": datetime.now(),
            }
            data.update(school.model_dump(by_alias=True))
            schools_data.append(data)
        return collection.insert_many(schools_data).inserted_ids
    
    def find(self, filter: Dict[str, Any], collection: Collection, max_docs: int = 5) -> List[School]:
        if not isinstance(filter, dict):
            raise ValueError(f"Input data expected to be a dictionary")
        
        cursor = collection.find(filter).limit(max_docs)
        schools = []

        for doc in cursor:
            school = School(
                church_id = doc["churchId"],
                school_id = doc["schoolId"],
                name = doc["name"],
                short_description = doc["shortDescription"],
                description = doc["description"],
                date_of_week = doc["dateOfWeek"],
                time = doc["time"],
                image_url = doc["imageUrl"],
                classes = [Class(**class_data) for class_data in doc["classes"]]
            )
            schools.append(school)
        cursor.close()

        if len(schools) >= 1:
            return schools
        return None