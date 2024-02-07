import pytest

import upandup as upup
from mashumaro import DataClassDictMixin
from mashumaro.mixins.yaml import DataClassYAMLMixin
from dataclasses import dataclass
import os
import glob

@dataclass
class DataSchema1(DataClassDictMixin):
    x: int

@dataclass
class DataSchema2(DataClassDictMixin):
    x: int
    y: int

@dataclass
class DataYaml1(DataClassYAMLMixin):
    x: int

@dataclass
class DataYaml2(DataClassYAMLMixin):
    x: int
    y: int

def clean_up():
    fnames = sorted(glob.glob("./TMP*"))
    for fname in fnames:
        if os.path.exists(fname):
            os.remove(fname)

def test_options_dict():
    clean_up()
    try:
        update_1_to_2 = lambda cls_start, cls_end, obj_start: cls_end(x=obj_start.x, y=0)

        # Register the update
        upup.register_updates("DataSchemaOptsDict", DataSchema1, DataSchema2, fn_update=update_1_to_2)

        data = {"x": 1}
        options = upup.LoadOptions(write_versions=True, write_version_prefix="TMP", write_versions_dir=".")
        obj = upup.load("DataSchemaOptsDict", data, options=options)
        assert os.path.exists("TMP_DataSchema2.json")
        assert type(obj) == DataSchema2
        assert obj.x == 1
        assert obj.y == 0
    
    finally:
        clean_up()

def test_options_yaml():
    clean_up()
    try:
        update_1_to_2 = lambda cls_start, cls_end, obj_start: cls_end(x=obj_start.x, y=0)

        # Register the update
        upup.register_updates("DataSchemaOptsYaml", DataYaml1, DataYaml2, fn_update=update_1_to_2)

        data = 'x: 3\n'
        options = upup.LoadOptions(write_versions=True, write_version_prefix="TMP", write_versions_dir=".")
        obj = upup.load("DataSchemaOptsYaml", data, options=options)
        assert os.path.exists("TMP_DataYaml1.yaml")
        assert os.path.exists("TMP_DataYaml2.yaml")
        assert type(obj) == DataYaml2
        assert obj.x == 3
        assert obj.y == 0
    
    finally:
        clean_up()
