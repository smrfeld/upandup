from enum import Enum


class Serializer(Enum):
    DICT = "dict"
    JSON = "json"
    ORJSON = "orjson"
    YAML = "yaml"
    TOML = "toml"


def check_serializer(cls) -> Serializer:
    if hasattr(cls, "to_dict") and hasattr(cls, "from_dict"):
        return Serializer.DICT
    elif hasattr(cls, "to_json") and hasattr(cls, "from_json"):
        return Serializer.JSON
    elif hasattr(cls, "to_json") and hasattr(cls, "from_json"):
        return Serializer.ORJSON
    elif hasattr(cls, "to_yaml") and hasattr(cls, "from_yaml"):
        return Serializer.YAML
    elif hasattr(cls, "to_toml") and hasattr(cls, "from_toml"):
        return Serializer.TOML
    else:
        raise AttributeError("Serializer class must have to_dict/from_dict or to_json/from_json methods")


def serialize_obj(obj: object, serializer: Serializer):
    if serializer == Serializer.DICT:
        assert hasattr(obj, "to_dict") and hasattr(obj, "from_dict"), f"Serializer class must have to_dict/from_dict methods"
        return obj.to_dict() # type: ignore
    elif serializer == Serializer.JSON:
        assert hasattr(obj, "to_json") and hasattr(obj, "from_json"), f"Serializer class must have to_json/from_json methods"
        return obj.to_json() # type: ignore
    elif serializer == Serializer.ORJSON:
        assert hasattr(obj, "to_orjson") and hasattr(obj, "from_orjson"), f"Serializer class must have to_orjson/from_orjson methods"
        return obj.to_orjson() # type: ignore
    elif serializer == Serializer.YAML:
        assert hasattr(obj, "to_yaml") and hasattr(obj, "from_yaml"), f"Serializer class must have to_yaml/from_yaml methods"
        return obj.to_yaml() # type: ignore
    elif serializer == Serializer.TOML:
        assert hasattr(obj, "to_toml") and hasattr(obj, "from_toml"), f"Serializer class must have to_toml/from_toml methods"
        return obj.to_toml() # type: ignore
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
    elif serializer == Serializer.ORJSON:
        assert hasattr(cls, "to_orjson") and hasattr(cls, "from_orjson"), f"Serializer class must have to_orjson/from_orjson methods"
        return cls.from_orjson(data) # type: ignore
    elif serializer == Serializer.YAML:
        assert hasattr(cls, "to_yaml") and hasattr(cls, "from_yaml"), f"Serializer class must have to_yaml/from_yaml methods"
        return cls.from_yaml(data) # type: ignore
    elif serializer == Serializer.TOML:
        assert hasattr(cls, "to_toml") and hasattr(cls, "from_toml"), f"Serializer class must have to_toml/from_toml methods"
        return cls.from_toml(data) # type: ignore
    else:
        raise ValueError(f"Unknown serializer: {serializer}")


def deserialize(data: dict, cls: type):
    serializer = check_serializer(cls)
    return deserialize_obj(data, cls, serializer)