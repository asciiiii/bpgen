import base64
import json
import os
import pathlib
import zlib


class CityBlock:
    def __init__(self, name):
        path = pathlib.Path(__file__).parent.absolute()
        path = os.path.join(path, 'blueprints', name + '.blueprint')

        with open(path) as f:
            b64 = f.read()[1:]

        gz = base64.b64decode(b64)
        data = zlib.decompress(gz)
        self.data = json.loads(data)

    def get_encoded(self):
        j = json.dumps(self.data)
        data = j.encode("utf8")
        gz = zlib.compress(data, level=9)
        b64 = base64.b64encode(gz)
        return '0' + b64.decode("ascii")

    def add_landfill(self):
        tiles = []

        for y in range(32 * 5):
            for x in range(32 * 7):
                tiles.append({
                    "position": {
                        "x": x,
                        "y": y
                    },
                    "name": "landfill"
                })

        self.data['blueprint']['tiles'] = tiles
