from enum import Enum

class Serializer(Enum):
    DICT = "dict"
    JSON = "json"

def check_serializer(cls) -> Serializer:
    if hasattr(cls, "to_dict") and hasattr(cls, "from_dict"):
        return Serializer.DICT
    elif hasattr(cls, "to_json") and hasattr(cls, "from_json"):
        return Serializer.JSON
    else:
        raise AttributeError("Serializer class must have to_dict/from_dict or to_json/from_json methods")

def serialize_obj(obj, serializer: Serializer):
    if serializer == Serializer.DICT:
        return obj.to_dict()
    elif serializer == Serializer.JSON:
        return obj.to_json()
    else:
        raise ValueError(f"Unknown serializer: {serializer}")

def serialize(cls, obj):
    serializer = check_serializer(cls)
    return serialize_obj(obj, serializer)

def deserialize_obj(data, cls, serializer: Serializer):
    if serializer == Serializer.DICT:
        return cls.from_dict(data)
    elif serializer == Serializer.JSON:
        return cls.from_json(data)
    else:
        raise ValueError(f"Unknown serializer: {serializer}")

def deserialize(data, cls):
    serializer = check_serializer(cls)
    return deserialize_obj(data, cls, serializer)