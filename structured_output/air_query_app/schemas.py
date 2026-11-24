from dataclasses import dataclass
from pydantic import BaseModel, Field



AIR_QUERY_SCHEMA = {
    "type" : "object",
    "properties" : {
        "location": {
            "type": ["string", "null"],
            "description": "Địa điểm người dùng đề cập." # hướng dẫn ý nghĩa cho mô hình
        },
        "indicator": {
            "type": "string",
            "enum": ["PM2.5", "PM10", "AQI", "CO", "NO2", "SO2", "O3"] # tập giá trị được phép
        },
        "operator": {
            "type": "string",
            "enum": ["gt", "gte", "lt", "lte", "eq"] 
        },
        "value": {
            "type": "number",
            "minimum": 0 # ràng buộc giá trị số
        }
    },
    "required": ["indicator", "operator", "value"] #danh sách các trường bắt buộc 
}

