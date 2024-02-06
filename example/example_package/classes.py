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

update_1_to_2 = lambda cls_start, cls_end, obj_start: cls_end(x=obj_start.x, y=0)

# Register the update
register_updates("DataScheme", DataSchema1, DataSchema2, fn_update=update_1_to_2)