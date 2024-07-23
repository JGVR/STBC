import pytest
from stbcApi.app.models.member import Member
from stbcApi.app.services.member_handler import MemberHandler
from pymongo import MongoClient
from stbcApi.app.config import config
from datetime import datetime
from bson import ObjectId

class TestMemberHandler:
    client = MongoClient(config.atlas_conn_str)
    db = client["churches"]
    collection = db["churchDetails"]

    def test_insert_member_with_correct_schema(self):  
        members = [
                Member(
                church_id=1,
                member_id=1,
                first_name="Juan",
                last_name="Vasquez",
                title="Softwate Dev",
                short_bio="Bilingual, born and raised in the DR",
                email_address=None,
                image_url="",
                start_date=datetime.now(),
                end_date=None
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
        
    def test_find_member(self):
        filter = {
            "memberId": 1
        }
        results = MemberHandler().find(filter, self.collection)
        assert isinstance(results, list)
        assert all(isinstance(member, Member) for member in results)
    
    def test_delete_member(self):
        filter = {
            "firstName": "John"
        }
        result = MemberHandler().delete(filter, self.collection)
        assert result["count"] == 1

    def test_update_member(self):
        filter = {
            "phoneNumber": None,
            "emailAddress": None
        }
        new_data = {
            "phoneNumber": "999-999-9999",
            "emailAddress": "test@gmail.com"
        }
        result = MemberHandler().update(filter, new_data, self.collection)
        assert result["count"] == 1