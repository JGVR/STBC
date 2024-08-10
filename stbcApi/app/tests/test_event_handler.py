import pytest
from stbcApi.app.models.event import Event
from stbcApi.app.services.event_handler import EventHandler
from stbcApi.app.config import config
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from pydantic_core import ValidationError

class TestEventHandler:
    client = MongoClient(config.atlas_conn_str)
    db = client["churches"]
    collection = db["churchDetails"]

    def test_insert_event_with_correct_schema(self):
        events = [
            Event(
                church_id=1,
                title="Test event title",
                description="This is a test for church events",
                date=datetime.now(),
                imageUrl="",
                location=""
            ),
            Event(
                church_id=1,
                title="Test event title 2",
                description="This is a test for church events 2",
                date=datetime.now(),
                imageUrl="",
                location=""
            )
        ]
        results = EventHandler().insert(events, self.collection)
        assert len(results) == 2
        assert all(isinstance(doc_id, ObjectId) for doc_id in results)

    def test_insert_event_with_incorrect_schema(self):
        with pytest.raises(ValidationError) as exc:
            events = [
                Event(
                    church_id=1,
                    title="Test event title 2",
                    description="This is a test for church events 2",
                    date=datetime.now(),
                    imageUrl="",
                    location="",
                    test="This should fail"
                )
            ]
            results = EventHandler().insert(events, self.collection)
        assert "validation error" in str(exc)

    def test_find_event_by_title(self):
        filter = {
            "churchId": 1,
            "title": "Test event title 2"
        }
        results = EventHandler().find(filter, self.collection)
        assert all(isinstance(event, Event) for event in results)
        assert len(results) == 2

    def test_find_non_existant_event(self):
        filter = {
            "churchId": 1,
            "title": "Test event title 55"
        }
        results = EventHandler().find(filter, self.collection)
        assert results == None

    def test_delete_event(self):
        filter = {
            "churchId": 1,
            "description": "This is a test for church events",
        }
        result = EventHandler().delete(filter, self.collection)
        assert result["count"] == 1
    
    def test_update_event(self):
        filter = {
            "churchId": 1,
            "title": "Test event title 2",
            "description": "This is a test for church events 2"
        }
        new_data = {
            "title": "Test event title 3",
            "description": "This is a test for church events 3"
        }
        result = EventHandler().update(filter, new_data, self.collection)
        assert result["count"] == 1
    