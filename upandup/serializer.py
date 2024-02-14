from enum import Enum
import os
from typing import Union
from loguru import logger


class Serializer(Enum):
    """Serialization formats.
    """    
    DICT = "dict"
    "Dictionary format."

    JSON = "json"
    "JSON format."

    YAML = "yaml"
    "YAML format."

    TOML = "toml"
    "TOML format."


def check_serializer(cls) -> Serializer:
    """Check the serializer for a class.

    Raises:
        AttributeError: Serializer class must have to_dict/from_dict or to_json/from_json methods

    Returns:
        Serializer: Serializer format.
    """    
    if hasattr(cls, "to_json") and hasattr(cls, "from_json"):
        return Serializer.JSON
    elif hasattr(cls, "to_yaml") and hasattr(cls, "from_yaml"):
        return Serializer.YAML
    elif hasattr(cls, "to_toml") and hasattr(cls, "from_toml"):
        return Serializer.TOML
    elif hasattr(cls, "to_dict") and hasattr(cls, "from_dict"):
        return Serializer.DICT
    else:
        raise AttributeError("Serializer class must have to_dict/from_dict or to_json/from_json methods")


def serialize_obj(obj: object, serializer: Serializer) -> Union[dict,str]:
    """Serialize an object.

    Args:
        obj (object): Object to serialize.
        serializer (Serializer): Serializer format.

    Raises:
        ValueError: Unknown serializer.

    Returns:
        Union[dict,str]: Serialized object.
    """    
    if serializer == Serializer.DICT:
        assert hasattr(obj, "to_dict") and hasattr(obj, "from_dict"), f"Serializer class must have to_dict/from_dict methods"
        return obj.to_dict() # type: ignore
    elif serializer == Serializer.JSON:
        assert hasattr(obj, "to_json") and hasattr(obj, "from_json"), f"Serializer class must have to_json/from_json methods"
        return obj.to_json() # type: ignore
    elif serializer == Serializer.YAML:
        assert hasattr(obj, "to_yaml") and hasattr(obj, "from_yaml"), f"Serializer class must have to_yaml/from_yaml methods"
        return obj.to_yaml() # type: ignore
    elif serializer == Serializer.TOML:
        assert hasattr(obj, "to_toml") and hasattr(obj, "from_toml"), f"Serializer class must have to_toml/from_toml methods"
        return obj.to_toml() # type: ignore
    else:
        raise ValueError(f"Unknown serializer: {serializer}")


def serialize(obj: object) -> Union[dict,str]:
    """Serialize an object.

    Args:
        obj (object): Object to serialize.

    Returns:
        Union[dict,str]: Serialized object.
    """    
    cls = type(obj)
    serializer = check_serializer(cls)
    return serialize_obj(obj, serializer)


def serialize_to_str(obj: object) -> str:
    """Serialize an object to a string, and not a dictionary (uses json.dumps to serialize to a string).

    Args:
        obj (object): Object to serialize.

    Raises:
        ValueError: Unknown type.

    Returns:
        str: Serialized object.
    """    
    d = serialize(obj)
    if type(d) == dict:
        import json
        return json.dumps(d)
    elif type(d) == str:
        return d
    else:
        raise ValueError(f"Unknown type: {type(d)}")


def deserialize_obj(data: Union[dict,str], cls: type, serializer: Serializer) -> object:
    """Deserialize an object.

    Args:
        data (Union[dict,str]): Data to deserialize.
        cls (type): Class to deserialize to.
        serializer (Serializer): Serializer format.

    Raises:
        ValueError: Unknown serializer.

    Returns:
        object: Deserialized object.
    """    
    if serializer == Serializer.JSON:
        assert hasattr(cls, "to_json") and hasattr(cls, "from_json"), f"Serializer class must have to_json/from_json methods"
        return cls.from_json(data) # type: ignore
    elif serializer == Serializer.YAML:
        assert hasattr(cls, "to_yaml") and hasattr(cls, "from_yaml"), f"Serializer class must have to_yaml/from_yaml methods"
        return cls.from_yaml(data) # type: ignore
    elif serializer == Serializer.TOML:
        assert hasattr(cls, "to_toml") and hasattr(cls, "from_toml"), f"Serializer class must have to_toml/from_toml methods"
        return cls.from_toml(data) # type: ignore
    elif serializer == Serializer.DICT:
        assert hasattr(cls, "to_dict") and hasattr(cls, "from_dict"), f"Serializer class must have to_dict/from_dict methods"
        assert type(data) == dict, f"Type of data must be dict, not {type(data)}: {data}"
        return cls.from_dict(data) # type: ignore
    else:
        raise ValueError(f"Unknown serializer: {serializer}")


def deserialize(data: Union[dict,str], cls: type) -> object:
    """Deserialize an object.

    Args:
        data (Union[dict,str]): Data to deserialize.
        cls (type): Class to deserialize to.

    Returns:
        object: Deserialized object.
    """    
    serializer = check_serializer(cls)    
    return deserialize_obj(data, cls, serializer)


def write_obj(obj: object, dir_name: str, bname_wo_ext: str):
    """Write an object to a file.

    Args:
        obj (object): Object to write.
        dir_name (str): Directory to write to.
        bname_wo_ext (str): Basename without extension.

    Raises:
        ValueError: Unknown serializer.
    """    
    cls = type(obj)
    serializer = check_serializer(cls)

    os.makedirs(dir_name, exist_ok=True)
    def file_path(ext: str):
        return os.path.join(dir_name, f"{bname_wo_ext}.{ext}")

    if serializer == Serializer.DICT:
        ext = "json"
    elif serializer == Serializer.JSON:
        ext = "json"
    elif serializer == Serializer.YAML:
        ext = "yaml"
    elif serializer == Serializer.TOML:
        ext = "toml"
    else:
        raise ValueError(f"Unknown serializer: {serializer}")

    fp = file_path(ext)
    with open(fp, "w") as f:
        f.write(serialize_to_str(obj))
