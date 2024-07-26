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
    client = MongoClient("mongodb+srv://jv_admin:Th0r3s3lDi0sDelTrueno1130!@portfolio.jmd2tdg.mongodb.net/?retryWrites=true&w=majority&appName=Portfolio")
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

    def test_insert_schools_with_incorrect_schema(self):
        with pytest.raises(ValidationError) as exc:
            schools = [
                School(
                    church_id=1,
                    school_id=2,
                    name="Wednesday School",
                    short_description = "testetstes",
                    date_of_week = "Wednesday",
                    description="test",
                    fail_field = 123456,
                    classes = [
                        Class(
                            member_ids = [1,2,3],
                            name="test",
                            ages = "9 to 10"
                        )
                    ]
                )
            ]
            results = SchoolHandler().insert(schools, self.collection)
        assert "Extra inputs are not permitted" in str(exc)


    def test_find_schools_with_same_classes(self):
        filter = {
            "churchId": 1,
            "classes.name": "Test Class"
        }
        results = SchoolHandler().find(filter, self.collection)
        assert isinstance(results, list)
        assert all(isinstance(school, School) for school in results)
        assert results[0].classes[0].name == "Test Class"
    
    def test_find_non_existant_school(self):
        filter ={
            "churchId": 1,
            "schoolId": 500
        }
        results = SchoolHandler().find(filter, self.collection)
        assert results == None

    def test_delete_school(self):
        filter = {
            "churchId": 1,
            "time": "22:25:55"
        }
        result = SchoolHandler().delete(filter, self.collection)
        assert result["count"] == 1

    def test_update_school(self):
        filter = {
            "churchId": 1,
            "schoolId": 2,
            "name": "Wednesday School",
            "time": "22:20:09"
        }
        new_data = {
            "name": "Wednesday Night School",
            "shortDescription": "Classes for Wednesday Night School",
            "description": "This is for Wednesday Night Schools",
            "dateOfWeek": "Wednesday"
        }
        result = SchoolHandler().update(filter, new_data, self.collection)
        assert result["count"] == 1