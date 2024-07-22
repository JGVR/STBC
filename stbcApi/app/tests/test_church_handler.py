import pytest
from stbcApi.app.models.church import Church
from stbcApi.app.services.church_handler import ChurchHandler
from stbcApi.app.config import config
from pymongo import MongoClient
from bson import ObjectId
from pydantic_core import ValidationError

class TestChurchHandler:
    client = MongoClient(config.atlas_conn_str)
    db = client["churches"]
    collection = db["churchDetails"]

    def test_insert_church_with_correct_schema(self):
        church = Church(churchId=1, name="Strong Tower Baptist Church")
        result = ChurchHandler().insert(church, self.collection)
        assert isinstance(result["_id"], ObjectId)
    
    def test_insert_church_with_long_name(self):
        with pytest.raises(ValidationError) as exc:
            church = Church(churchId=1, name="Strong Tower Baptist Church, Strong Tower Baptist Church, Strong Tower Baptist Church, Strong Tower Baptist Church,Strong Tower Baptist Church, Strong Tower Baptist Church, Strong Tower Baptist Church, Strong Tower Baptist Church, Strong Tower Baptist Church,Strong Tower Baptist Church, Strong Tower Baptist Church, Strong Tower Baptist Church, Strong Tower Baptist Church, Strong Tower Baptist Church,Strong Tower Baptist Church")
            result = ChurchHandler().insert(church, self.collection)
            
        assert "validation error" in str(exc)
    
    def test_find_church_by_id(self):
        filter = {
            "churchId": 1
        }
        result = ChurchHandler().find(filter, self.collection)
        assert isinstance(result, Church)
        assert result.church_id == 1
    
    def test_find_non_existant_church(self):
        filter = {
            "churchId": 50
        }
        result = ChurchHandler().find(filter, self.collection)
        assert result == None
    
    def test_delete_church(self):
        filter = {
            "churchId": 1
        }
        result = ChurchHandler().delete(filter, self.collection)
        assert result["count"] == 1
    
    def test_delete_non_existant_church(self):
        filter = {
            "churchId": 50
        }
        result = ChurchHandler().delete(filter, self.collection)
        assert result["count"] == 0

    def test_update_church_name(self):
        filter = {
            "type": "church",
            "name": "Strong Tower Baptist Church"
        }
        new_data = {
            "name": "First Baptist Church"
        }
        result = ChurchHandler().update(filter, new_data, self.collection)
        assert result["count"] == 1
    
    def test_update_non_existant_church(self):
        filter = {
            "type": "church",
            "name": "IBI"
        }
        new_data = {
            "name": "Saint John Church"
        }
        result = ChurchHandler().update(filter, new_data, self.collection)
        assert result["count"] == 0