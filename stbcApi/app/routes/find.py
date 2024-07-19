from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..services.handler_identifier import HandlerIdentifier
from ..config import config
from pymongo import MongoClient

@api_view(["GET"])
def find(request):
    try:
        client = MongoClient(config.atlas_conn_str)
        db = client[config.atlas_db_name]
        collection = db[config.atlas_collection_name]
        req_data = request.query_params
        handler = HandlerIdentifier.call(req_data["type"])
        resp = handler.find(req_data["model_data"], collection)
        return Response(resp, status.HTTP_200_OK, content_type="application/json")
    except Exception as ex:
        return Response(f"Error: {ex}", status.HTTP_400_BAD_REQUEST)
