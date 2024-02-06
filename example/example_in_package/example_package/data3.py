from mashumaro import DataClassDictMixin
from dataclasses import dataclass

@dataclass
class DataSchema3(DataClassDictMixin):
    x: int
    name: str