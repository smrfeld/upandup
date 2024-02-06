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

def serialize_obj(obj: object, serializer: Serializer):
    if serializer == Serializer.DICT:
        assert hasattr(obj, "to_dict") and hasattr(obj, "from_dict"), f"Serializer class must have to_dict/from_dict methods"
        return obj.to_dict() # type: ignore
    elif serializer == Serializer.JSON:
        assert hasattr(obj, "to_json") and hasattr(obj, "from_json"), f"Serializer class must have to_json/from_json methods"
        return obj.to_json() # type: ignore
    else:
        raise ValueError(f"Unknown serializer: {serializer}")

def serialize(obj: object) -> dict:
    cls = type(obj)
    serializer = check_serializer(cls)
    return serialize_obj(obj, serializer)

def deserialize_obj(data: dict, cls: type, serializer: Serializer):
    if serializer == Serializer.DICT:
        assert hasattr(cls, "to_dict") and hasattr(cls, "from_dict"), f"Serializer class must have to_dict/from_dict methods"
        return cls.from_dict(data) # type: ignore
    elif serializer == Serializer.JSON:
        assert hasattr(cls, "to_json") and hasattr(cls, "from_json"), f"Serializer class must have to_json/from_json methods"
        return cls.from_json(data) # type: ignore
    else:
        raise ValueError(f"Unknown serializer: {serializer}")

def deserialize(data: dict, cls: type):
    serializer = check_serializer(cls)
    return deserialize_obj(data, cls, serializer)