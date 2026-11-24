def parse_with_split(text: str) -> dict[str, str]: 
    result: dict[str, str] = {} 

    for part in text.split(";"): 
        key, value = part.split(":", maxsplit=1) 
        result[key.strip()] = value.strip() 

    return result 

samples = [ 
    "location: Hà Nội; indicator: PM2.5; value: 50", 
    "indicator: PM2.5; value: 50; location: Hà Nội", 
    "Địa điểm: Hà Nội, chỉ số PM2.5 lớn hơn 50", 
    "location=Hà Nội | indicator=PM2.5 | value=50", 
    '{"location": "Hà Nội", "indicator": "PM2.5", "value": 50}', 
] 

for sample in samples: 
    try: 
        print(parse_with_split(sample)) 
    except Exception as error: 
        print(type(error).__name__, error)