import pytest
from stbcApi.app.models.member import Member
from stbcApi.app.services.member_handler import MemberHandler
from pymongo import MongoClient
from stbcApi.app.config import config
from datetime import datetime

class TestMemberHandler:
    client = MongoClient(config.atlas_conn_str)
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
                email_address= "juangabrielvasquez11@gmail.com",
                image_url="",
                start_date = datetime.now(),
                end_date = None
            )
        ]
        result = MemberHandler().insert(members, self.collection)
        assert isinstance(result, list)
        assert 1 in result