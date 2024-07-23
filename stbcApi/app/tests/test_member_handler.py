import pytest
from stbcApi.app.models.member import Member
from stbcApi.app.services.member_handler import MemberHandler
from pymongo import MongoClient
from stbcApi.app.config import config
from datetime import datetime
from bson import ObjectId

class TestMemberHandler:
    client = MongoClient( "mongodb+srv://jv_admin:Th0r3s3lDi0sDelTrueno1130!@portfolio.jmd2tdg.mongodb.net/?retryWrites=true&w=majority&appName=Portfolio")
    db = client["churches"]
    collection = db["churchDetails"]

    def test_insert_member_with_correct_schema(self):  
        members = [
                Member(
                church_id=1,
                member_id = 1,
                first_name = "Juan",
                last_name = "Vasquez",
                title = "Softwate Dev",
                short_bio= "Bilingual, born and raised in the DR",
                email_address=None,
                image_url="",
                start_date = datetime.now(),
                end_date = None
            )
        ]
        result = MemberHandler().insert(members, self.collection)
        assert isinstance(result, list)
        assert isinstance(result[0], ObjectId)

    def test_insert_multiple_members(self):
        members = [
            Member(
                church_id=1,
                member_id = 2,
                first_name = "John",
                last_name = "Doe",
                title = "Preacher",
                short_bio= "2ND Year preacher",
                email_address= "johndoe@gmail.com",
                phone_number = "444-555-5565",
                image_url="",
                start_date = None,
                end_date = None
            ),
            Member(
                church_id=1,
                member_id = 3,
                first_name = "Jennifer",
                middle_name = "Brooke",
                last_name = "Doe",
                title = "Decon",
                short_bio= "2rd year decon",
                email_address= "jenniferdoe@gmail.com",
                phone_number = "444-555-5555",
                image_url="",
                start_date = None,
                end_date = None
            )
        ]
        result = MemberHandler().insert(members, self.collection)
        assert isinstance(result[0], ObjectId)
        assert isinstance(result[0], ObjectId)
        
    def test_find_church(self):
        filter = {
            "churchId": 1
        }
        results = MemberHandler().find(filter, self.collection)
        assert isinstance(results, list)
        assert all(isinstance(member, Member) for member in results)
