from .handler import Handler
from ..models.member import Member
from pymongo.collection import Collection
from typing import Dict, Any, List
from ..utils.type import Type
from datetime import datetime
from bson import ObjectId

class MemberHandler(Handler):
    def insert(self, members: List[Member], collection: Collection) -> List[int]:
        if not all(isinstance(member, Member) for member in members):
            raise ValueError(f"Input data expected to be a list of member objects.")
        
        members_data = []
        for member in members:
            data = {
                "_id": ObjectId(),
                "type": Type.MEMBER.value,
                "createdAt": datetime.now()
            }
            data.update(member.model_dump(by_alias=True))
            members_data.append(data)
        return collection.insert_many(members_data).inserted_ids
    
    def find(self, filter: Dict[str, Any], collection: Collection, max_docs: int = 5) -> List[Member]:
        if not isinstance(filter, dict):
            raise ValueError(f"Input data expected to be a dictionary")
        
        cursor = collection.find(filter).limit(max_docs)
        members = []

        for doc in cursor:
            member = Member(
                church_id = doc["churchId"],
                member_id = doc["memberId"],
                firstName = doc["firstName"],
                middleName = doc["middleName"],
                lastName = doc["lastName"],
                title = doc["title"],
                short_bio = doc["shortBio"],
                email_address = doc["emailAddress"],
                phone_number = doc["phoneNumber"],
                imageUrl = doc["imageUrl"],
                start_date = doc["startDate"],
                end_date = doc["endDate"]
            )
            members.append(member)
        cursor.close()

        if len(members) >= 1:
            return members
        return None