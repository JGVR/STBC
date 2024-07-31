import pytest
from stbcApi.app.models.ministry import Ministry
from stbcApi.app.services.ministry_handler import MinistryHandler
from stbcApi.app.config import config
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from pydantic_core import ValidationError

class TestMinistryHandler:
    client = MongoClient(config.atlas_conn_str)
    db = client["churches"]
    collection = db["churchDetails"]

    def test_insert_ministry_with_correct_schema(self):
        ministries = [
            Ministry(
                church_id=1,
                name="Test Ministry 1",
                description="This is the description of test ministry 1",
                image_url="",
                register_url=""
            ),
            Ministry(
                church_id=1,
                name="Test Ministry 2",
                description="This is the description of test ministry 2",
            )
        ]
        results = MinistryHandler().insert(ministries, self.collection)
        assert isinstance(results, list)
        assert all(isinstance(id, ObjectId) for id in results)

    def test_insert_ministry_with_incorrect_schema(self):
        with pytest.raises(ValidationError) as exc:
            ministries = [
                Ministry(
                    church_id=1,
                    name="Test Ministry 2",
                    description="This is the description of test ministry 2",
                    test="this should fail."
                )
            ]
            results = MinistryHandler().insert(ministries, self.collection)
        assert "validation error" in str(exc)

    def test_find_ministry_by_name(self):
        filter = {
            "name": "Test Ministry 2"
        }
        results = MinistryHandler().find(filter, self.collection)
        assert len(results) == 5
        assert all(isinstance(ministry, Ministry) for ministry in results)

    def test_find_ministry_by_description(self):
        filter = {
            "description": "This is the description of test ministry 1"
        }
        results = MinistryHandler().find(filter, self.collection)
        assert len(results) == 5
        assert all(isinstance(ministry, Ministry) for ministry in results)

    def test_delete_ministry(self):
        filter = {
            "churchId": 1,
            "name": "Test Ministry 2"
        }
        result = MinistryHandler().delete(filter, self.collection)
        assert result["count"] == 1

    def test_update_school(self):
        filter = {
            "churchId": 1,
            "description": "This is the description of test ministry 1"
        }
        new_data = {
            "name": "Test Ministry 3",
            "description": "This is the description of test ministry 3",
            "imageUrl": "test",
            "registerUrl": "test"
        }
        result = MinistryHandler().update(filter, new_data, self.collection)
        assert result["count"] == 1