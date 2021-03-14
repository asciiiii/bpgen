import base64
import json
import zlib
from struct import pack
from struct import unpack

from bpgen.factorio.generated.signals import SIGNAL_RAIL

FACTORIO_VERSION = (0, 21, 1, 1)


class Blueprint:
    def __init__(self):
        self.entities = []

    def encode_version_string(self, major, minor, patch, dev):
        b = pack('HHHH', major, minor, patch, dev)
        return int.from_bytes(b, byteorder='big', signed=False)

    def decode_version_string(self, value):
        b = value.to_bytes(8, 'little')
        return unpack('HHHH', b)

    def add_entity(self, entity):
        self.entities.append(entity)

    def get_encoded(self):
        data = self.generate().encode("utf8")
        gz = zlib.compress(data)
        b64 = base64.b64encode(gz)
        return '0' + b64.decode("ascii")

    def generate(self):
        data = {
            "blueprint": {
                "item": "blueprint",
                "version": self.encode_version_string(*FACTORIO_VERSION),
                "icons": [
                    {
                        "index": 1,
                        "signal": SIGNAL_RAIL.get_json(),
                    }
                ],
                "entities": [entity.generate() for entity in self.entities],
            }
        }
        return json.dumps(data, indent=4)
