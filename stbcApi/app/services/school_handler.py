from .handler import Handler
from ..models.school import School
from ..models.church_class import Class
from pymongo.collection import Collection
from typing import Dict, Any, List
from ..utils.type import Type
from datetime import datetime
from bson import ObjectId

class SchoolHandler(Handler):
    def insert(self, schools: List[School], collection: Collection) -> List[str]:
        if not all(isinstance(school, School) for school in schools):
            raise ValueError(f"Input data expected to be a list of School objects.")
        
        schools_data = []
        last_doc = collection.find_one(filter={"type": "ministry"}, sort=[("recordId", -1)])
        last_id = last_doc["recordId"] if last_doc else 0

        for school in schools:
            last_id+=1
            data = {
                "_id": ObjectId(),
                "type": Type.SCHOOL.value,
                "createdAt": datetime.now(),
                "schoolId": last_id
            }
            data.update(school.model_dump(by_alias=True, exclude={"school_id"}))
            schools_data.append(data)
        return [str(id) for id in collection.insert_many(schools_data).inserted_ids]
    
    def find(self, filter: Dict[str, Any], collection: Collection, max_docs: int = 5) -> List[School]:
        if not isinstance(filter, dict):
            raise ValueError(f"Input data expected to be a dictionary")
        school_id = filter.pop("schoolId",0)
        
        cursor = collection.find({
            **filter,
            "schoolId": {"$gt": school_id}
        }, sort=[("schoolId", 1)]).limit(max_docs)
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