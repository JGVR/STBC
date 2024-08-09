from typing import Dict, Any
from datetime import datetime

class QueryParamParser:
    @staticmethod
    def call(query_params) -> Dict[str, Any]:
        # > query_params will be an instance of django QueryDict
        data = {}
        for key in query_params.keys():
            if "id" in key or "Id" in key:
                data[key] = int(query_params[key])
            else:
                data[key] = query_params[key]
        return data