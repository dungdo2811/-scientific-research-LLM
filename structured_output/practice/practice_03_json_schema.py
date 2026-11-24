from jsonschema import ValidationError, validate 
from air_query_app.schemas import AIR_QUERY_SCHEMA

samples = [ 
    { 
        "location": "Hà Nội", 
        "indicator": "PM2.5", 
        "operator": "gt", 
        "value": 50, 
    }, 
    { 
        "location": "Hà Nội", 
        "operator": "gt", 
        "value": 50, 
    }, 
    { 
        "location": "Hà Nội", 
        "indicator": "PM2.5", 
        "operator": "gt", 
        "value": -1, 
    }, 
] 

for index, sample in enumerate(samples, start=1): 
    try: 
        validate(instance=sample, schema= AIR_QUERY_SCHEMA) 
        print(index, "VALID") 
    except ValidationError as error: 
        print(index, "INVALID", list(error.path), error.message) 