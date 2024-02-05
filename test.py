from mashumaro.mixins.json import DataClassJSONMixin
from dataclasses import dataclass

@dataclass
class Data(DataClassJSONMixin):

    x: int

d = Data(x=3).to_json()
print(d)