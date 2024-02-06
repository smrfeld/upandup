import pytest

import upanddown as updn
from mashumaro import DataClassDictMixin
from dataclasses import dataclass

@dataclass
class DataSchema1(DataClassDictMixin):
    x: int

@dataclass
class DataSchema2(DataClassDictMixin):
    x: int
    y: int

@dataclass
class DataSchema2alt(DataClassDictMixin):
    x: int
    y: int = 3

def test_simple():

    update_1_to_2 = lambda cls_start, cls_end, obj_start: cls_end(x=obj_start.x, y=0)

    # Register the update
    updn.register_updates("DataSchemaSimple", DataSchema1, DataSchema2, fn_update=update_1_to_2)

    data = {"x": 1}
    obj = updn.load("DataSchemaSimple", data)
    assert type(obj) == DataSchema2
    assert obj.x == 1
    assert obj.y == 0
    print(obj)

def test_alt():

    update_1_to_2 = lambda cls_start, cls_end, obj_start: cls_end(x=obj_start.x)

    # Register the update
    updn.register_updates("DataSchemaAlt", DataSchema1, DataSchema2alt, fn_update=update_1_to_2)

    data = {"x": 1}
    obj = updn.load("DataSchemaAlt", data)
    assert type(obj) == DataSchema2alt
    assert obj.x == 1
    assert obj.y == 3
    print(obj)

def test_incomplete_updates():

    update_1_to_2 = lambda cls_start, cls_end, obj_start: cls_end(x=obj_start.x)

    # Register the update
    updn.register_updates("DataSchemaIncomplete", DataSchema1, DataSchema2, fn_update=update_1_to_2)

    data = {"x": 1}
    with pytest.raises(TypeError):
        _ = updn.load("DataSchemaIncomplete", data)

