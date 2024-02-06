from upanddown import register_updates
from mashumaro import DataClassDictMixin
from dataclasses import dataclass

@dataclass
class DataSchema1(DataClassDictMixin):
    x: int

@dataclass
class DataSchema2(DataClassDictMixin):
    x: int
    y: int
    z: int = 0

@dataclass
class DataSchema3(DataClassDictMixin):
    x: int
    name: str

update_1_to_2 = lambda cls_start, cls_end, obj_start: cls_end(x=obj_start.x, y=0)
update_2_to_3 = lambda cls_start, cls_end, obj_start: cls_end(x=obj_start.x, name="default")

# Register the update
register_updates("DataScheme", DataSchema1, DataSchema2, fn_update=update_1_to_2)
register_updates("DataScheme", DataSchema2, DataSchema3, fn_update=update_2_to_3)