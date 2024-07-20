import pytest
from stbcApi.app.models.church import Church
from stbcApi.app.services.church_handler import ChurchHandler
from stbcApi.app.config import config
from pymongo import MongoClient
from bson import ObjectId
from pydantic_core import ValidationError

class TestChurchHandler:
    client = MongoClient("mongodb+srv://jv_admin:Th0r3s3lDi0sDelTrueno1130!@portfolio.jmd2tdg.mongodb.net/?retryWrites=true&w=majority&appName=Portfolio")
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