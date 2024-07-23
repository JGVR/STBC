import pytest
from stbcApi.app.models.devotion import Devotion
from stbcApi.app.services.devotion_handler import DevotionHandler
from stbcApi.app.config import config
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

class TestChurchHandler:
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