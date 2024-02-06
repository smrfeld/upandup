from mashumaro import DataClassDictMixin
from dataclasses import dataclass

@dataclass
class DataSchema1(DataClassDictMixin):
    x: int