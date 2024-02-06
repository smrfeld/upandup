from mashumaro import DataClassDictMixin
from dataclasses import dataclass

@dataclass
class DataSchema2(DataClassDictMixin):
    x: int
    y: int
    z: int = 0