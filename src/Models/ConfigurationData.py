from dataclasses import dataclass
from dataclasses import field

from dataclasses_json import config
from dataclasses_json import dataclass_json
from dataclasses_json import LetterCase


@dataclass_json
@dataclass
class ConfigurationData:
    hostname: str
    port: str
    api_key: str = field(metadata=config(letter_case=LetterCase.CAMEL))
