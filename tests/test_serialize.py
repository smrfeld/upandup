import pytest

import upandup as upup
from mashumaro import DataClassDictMixin
from mashumaro.mixins.yaml import DataClassYAMLMixin
from mashumaro.mixins.json import DataClassJSONMixin
from mashumaro.mixins.toml import DataClassTOMLMixin
from dataclasses import dataclass

@dataclass
class DataDict(DataClassDictMixin):
    x: int

@dataclass
class DataYaml(DataClassYAMLMixin):
    x: int

@dataclass
class DataJson(DataClassJSONMixin):
    x: int

@dataclass
class DataToml(DataClassTOMLMixin):
    x: int

@pytest.mark.parametrize("cls", [DataDict, DataYaml, DataJson, DataToml])
def test_dict(cls):
    data = cls(x=1)
    d = upup.serialize(data)
    if cls in [DataDict]:
        assert d == {"x": 1}
    elif cls in [DataJson]:
        assert d == '{"x": 1}'
    elif cls in [DataYaml]:
        assert d == "x: 1\n"
    elif cls in [DataToml]:
        assert d == "x = 1\n"
    else:
        raise ValueError(f"Unknown class: {cls}")

    data_repr = upup.deserialize(d, cls)
    assert data_repr == data