from mashumaro import DataClassDictMixin
from dataclasses import dataclass

@dataclass
class DataSchemaV1(DataClassDictMixin):
    x: int