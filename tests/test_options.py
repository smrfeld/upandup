import pytest

import upandup as upup
from mashumaro import DataClassDictMixin
from dataclasses import dataclass
import os

@dataclass
class DataSchema1(DataClassDictMixin):
    x: int

@dataclass
class DataSchema2(DataClassDictMixin):
    x: int
    y: int

def clean_up():
    fnames = ["TMP_DataSchema2.json"]
    for fname in fnames:
        if os.path.exists(fname):
            os.remove(fname)

def test_options():
    clean_up()
    try:
        update_1_to_2 = lambda cls_start, cls_end, obj_start: cls_end(x=obj_start.x, y=0)

        # Register the update
        upup.register_updates("DataSchemaOpts", DataSchema1, DataSchema2, fn_update=update_1_to_2)

        data = {"x": 1}
        options = upup.Options(write_versions=True, write_version_prefix="TMP", write_versions_dir=".")
        obj = upup.load("DataSchemaOpts", data, options=options)
        assert os.path.exists("TMP_DataSchema2.json")
        assert type(obj) == DataSchema2
        assert obj.x == 1
        assert obj.y == 0
    
    finally:
        clean_up()
