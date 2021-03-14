import base64
import json
import os
import pathlib
import zlib


def replace_item(obj, key, value_mapping):
    for k, v in obj.items():
        if isinstance(v, dict):
            obj[k] = replace_item(v, key, value_mapping)
        elif isinstance(v, list):
            if isinstance(v[0], dict):
                obj[k] = [replace_item(e, key, value_mapping) for e in v]

    if key in obj:
        if obj[key] in value_mapping:
            obj[key] = value_mapping[obj[key]]

    return obj


class CityBlock:
    def __init__(self, name):
        path = pathlib.Path(__file__).parent.absolute()
        path = os.path.join(path, 'blueprints', name + '.blueprint')

        with open(path) as f:
            b64 = f.read()[1:]

        gz = base64.b64decode(b64)
        data = zlib.decompress(gz)
        self.data = json.loads(data)

    def get_last_id(self):
        m = 0

        for entity in self.data['blueprint']['entities']:
            m = max(m, entity['entity_number'])

        return m

    def get_next_id(self):
        return self.get_last_id() + 1

    def add_entities(self, entities, o, out=True):
        id_map = {}
        for entity in entities:
            old_id = entity['entity_number']
            entity['entity_number'] = self.get_next_id()
            id_map[old_id] = entity['entity_number']

            if out:
                entity['position']['x'] += (32 * 6) - (10 * o) - 2
            else:
                entity['position']['x'] += (32 * 1) + (10 * (o - 1))

            entity['position']['y'] += 18
            self.data['blueprint']['entities'].append(entity)

        for entity in entities:
            if 'neighbours' in entity:
                neighbours = entity['neighbours']
                entity['neighbours'] = []
                for n in neighbours:
                    entity['neighbours'].append(id_map[n])

            if 'connections' in entity:
                entity['connections'] = replace_item(entity['connections'], 'entity_id', id_map)

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
