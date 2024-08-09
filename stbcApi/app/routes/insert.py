from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..services.handler_identifier import HandlerIdentifier
from ..services.model_identifier import ModelIdentifier
from ..config import config
from pymongo import MongoClient

@api_view(['POST'])
def insert(request):
    try:
        client = MongoClient(config.atlas_conn_str)
        db = client[config.atlas_db_name]
        collection = db[config.atlas_collection_name]
        handler = HandlerIdentifier.call(request.data["type"])
        resp = None

        if isinstance(request.data["model_data"], dict):
            model = ModelIdentifier.call(request.data["type"], request.data["model_data"])
            resp = handler.insert(model, collection)
        else:
            model_data = []
            for data in request.data["model_data"]:
                model = ModelIdentifier.call(request.data["type"], data)
                model_data.append(model)
            resp = handler.insert(model_data, collection)

        return Response(resp, status.HTTP_201_CREATED, content_type="application/json")
    except Exception as ex:
        return Response(f"Error: {ex}", status.HTTP_400_BAD_REQUEST)