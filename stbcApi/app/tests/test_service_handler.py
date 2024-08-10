import pytest
from stbcApi.app.models.service import Service
from stbcApi.app.services.service_handler import ServiceHandler
from stbcApi.app.config import config
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from pydantic_core import ValidationError

class TestServiceHandler:
    client = MongoClient(config.atlas_conn_str)
    db = client["churches"]
    collection = db["churchDetails"]

    def test_insert_service_with_correct_schema(self):
        services = [
            Service(
                church_id=1,
                title="Test Service I",
                date_of_week="Wednesday",
                time=datetime.now().strftime("%H:%M:%S")
            ),
            Service(
                church_id=1,
                title="Test Service II",
                date_of_week="Saturday",
                time=datetime.now().strftime("%H:%M:%S")
            )
        ]
        results = ServiceHandler().insert(services, self.collection)
        assert isinstance(results, list)
        assert all(isinstance(id, ObjectId) for id in results)

    def test_insert_service_with_incorrect_schema(self):
        with pytest.raises(ValidationError) as exc:
            services = [
                Service(
                    church_id=1,
                    title="Test Service III",
                    date_of_week="Saturday",
                    time=datetime.now().strftime("%H:%M:%S"),
                    test="This should fail."
                )
            ]
            results = ServiceHandler().insert(services, self.collection)
        assert "validation error" in str(exc)

    def test_find_service_by_title(self):
        filter = {
            "title": "Test Service II"
        }
        results = ServiceHandler().find(filter, self.collection)
        assert len(results) == 5
        assert all(isinstance(service, Service) for service in results)

    def test_delete_service(self):
        filter = {
            "churchId": 1,
             "title": "Test Service II"
        }
        result = ServiceHandler().delete(filter, self.collection)
        assert result["count"] == 1

    def test_update_service(self):
        filter = {
            "churchId": 1,
            "title": "Test Service I"
        }
        new_data = {
            "title": "Test Service III",
            "dateOfWeek": "Sunday",
            "time": datetime.now().strftime("%H:%M:%S")
        }
        result = ServiceHandler().update(filter, new_data, self.collection)
        assert result["count"] == 1