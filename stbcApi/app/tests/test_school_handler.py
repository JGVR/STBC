import pytest
from stbcApi.app.models.school import School
from stbcApi.app.models.church_class import Class
from stbcApi.app.services.school_handler import SchoolHandler
from stbcApi.app.config import config
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from pydantic_core import ValidationError

class TestSchoolHandler:
    client = MongoClient(config.atlas_conn_str)
    db = client["churches"]
    collection = db["churchDetails"]

    def test_insert_school_with_correct_schema(self):
        schools = [
            School(
                church_id = 1,
                school_id = 1,
                name = "Wednesday School",
                short_description = "Sunday School",
                description = "This is for Sunday school classes",
                date_of_week = "Sunday",
                time = datetime.now().strftime("%H:%M:%S"),
                image_url = "",
                classes = [
                    Class(
                        member_ids=[1,2],
                        name="Test Class",
                        ages="From 2 to 4 years old."
                    ),
                    Class(
                        member_ids=[4,5,6,7],
                        name="Test Class 2",
                        ages="Adults of any ages"
                    ),
                ]
            ),
            School(
                church_id = 1,
                school_id = 2,
                name = "Wednesday School",
                short_description = "Wednesday School",
                description = "This is for Wednesday school classes",
                date_of_week = "Wednesday",
                time = datetime.now().strftime("%H:%M:%S"),
                image_url = "",
                classes = [
                    Class(
                        member_ids=[1,2],
                        name="Test Class",
                        ages="From 2 to 4 years old."
                    ),
                    Class(
                        member_ids=[4,5,6,7],
                        name="Test Class 2",
                        ages="Adults of any ages"
                    ),
                ]
            )
        ]
        results = SchoolHandler().insert(schools, self.collection)
        assert isinstance(results, list)
        assert isinstance(results[0], ObjectId)