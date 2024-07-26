import pytest
from stbcApi.app.models.devotion import Devotion
from stbcApi.app.services.devotion_handler import DevotionHandler
from stbcApi.app.config import config
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from pydantic_core import ValidationError

class TestDevotionHandler:
    client = MongoClient(config.atlas_conn_str)
    db = client["churches"]
    collection = db["churchDetails"]

    def test_insert_devotion_with_correct_schema(self):
        devotion = Devotion(
            church_id=1,
            member_id=2,
            title="test devotion",
            date=datetime.now(),
            message="test message for devotion test"
        )
        result = DevotionHandler().insert(devotion, self.collection)
        assert isinstance(result["_id"], ObjectId)

    def test_insert_devotion_with_incorrect_schema(self):
        with pytest.raises(ValidationError) as exc:
            devotion = Devotion(
                church_id=1,
                member_id=5,
                title="test devotion II",
                message="test message for devotion test II",
                test="this should fail"
            )
            result = DevotionHandler().insert(devotion, self.collection)
        assert "validation error" in str(exc)
        
    def test_find_devotion(self):
        filter = {
            "churchId": 1,
            "memberId": 2,
            "title": "test devotion"
        }
        result = DevotionHandler().find(filter, self.collection)
        assert isinstance(result, list)
        assert result[0].title == "test devotion"

    def test_delete_devotion(self):
        filter = {
            "churchId": 1,
            "memberId": 2,
            "title": "test devotion"
        }
        result = DevotionHandler().delete(filter, self.collection)
        assert result["count"] == 1

    def test_update_devotio(self):
        filter = {
            "churchId": 1,
            "memberId": 2,
            "title": "test devotion"
        }
        new_data = {
            "memberId": 55
        }
        result = DevotionHandler().update(filter, new_data, self.collection)
        assert result["count"] == 1