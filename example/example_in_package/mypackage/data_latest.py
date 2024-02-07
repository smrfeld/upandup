from mashumaro import DataClassDictMixin
from dataclasses import dataclass

@dataclass
class DataSchema(DataClassDictMixin):
    x: int
    name: str