from pydantic import BaseModel, Field 
from typing import Literal 

class AirQualityQuery(BaseModel): 
    location: str | None = Field( 
        default=None, 
        description="Địa điểm được nhắc trong câu hỏi." 
    ) 
    indicator: Literal[ 
        "PM2.5", "PM10", "AQI", "CO", "NO2", "SO2", "O3" 
    ] 
    operator: Literal["gt", "gte", "lt", "lte", "eq"] 
    value: float = Field(ge=0) 

print(AirQualityQuery.model_json_schema())