import pytest
from stbcApi.app.models.church import Church
from stbcApi.app.services.church_handler import ChurchHandler
from stbcApi.app.config import config
from pymongo import MongoClient
from bson import ObjectId
class TestChurchHandler:
    client = MongoClient(config.atlas_conn_str)
    db = client["churches"]
    collection = db["churchDetails"]

    def test_insert_church(self):
        church = Church(churchId=1, name="Strong Tower Baptist Church")
        result = ChurchHandler().insert(church, self.collection)
        assert isinstance(result["_id"], ObjectId)