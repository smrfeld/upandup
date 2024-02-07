from mashumaro import DataClassDictMixin
from dataclasses import dataclass

@dataclass
class DataSchemaV2(DataClassDictMixin):
    x: int
    y: int
    z: int = 0