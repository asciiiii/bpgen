import math

from bpgen.factorio.generated.signals import SIGNALS

WIRE_RED = 'red'
WIRE_GREEN = 'green'


def generate_combinator_text(text_line_1, text_line_2):
    line_max = max(len(text_line_1), len(text_line_2))

    text_line_1 = text_line_1.upper()
    text_line_2 = text_line_2.upper()

    # Normalize text length with space
    line_max += line_max % 2
    formatter = '{:' + str(line_max) + '}'
    text_line_1 = formatter.format(text_line_1)
    text_line_2 = formatter.format(text_line_2)

    entity_count = math.ceil(line_max / 2)

    entities = []

    for i in range(entity_count):
        ptr = i * 2
        entity = SignEntity(text_line_1[ptr:ptr + 2] + text_line_2[ptr:ptr + 2])
        entity.pos_x = i * entity.width
        entities.append(entity)

    return entities


class Entity:
    last_id = 0

    def __init__(self, name, width, height, connection_points=1):
        self.name = name
        self.width = width
        self.height = height
        # https://wiki.factorio.com/Blueprint_string_format#Connection_object
        # Most have 1 some 2
        self.connection_points = connection_points

        self.pos_x = 0
        self.pos_y = 0
        self.direction = 0
        self.connections = {}

        Entity.last_id += 1
        self.id = Entity.last_id

    def generate(self):
        return {
            "entity_number": self.id,
            "name": self.name,
            "position": {
                "x": self.pos_x + self.width / 2,
                "y": self.pos_y + self.height / 2
            },
            "connections": self.connections,
            "direction": self.direction,
            "control_behavior": self.get_control_behavior(),
        }

    def get_control_behavior(self):
        return {}


class ConstantCombinator(Entity):
    @staticmethod
    def new(signal, count=0):
        cc = ConstantCombinator()
        cc.add_signal(signal, count)
        return cc

    def __init__(self):
        super().__init__("constant-combinator", 1, 1)
        self.filters = []

    def new_filter_index(self):
        return len(self.filters) + 1

    def add_signal(self, signal, count=0):
        self.filters.append({
            "index": self.new_filter_index(),
            "signal": signal.get_json(),
            "count": count,
        })

    def get_control_behavior(self):
        return {
            'filters': self.filters
        }


class SignEntity(ConstantCombinator):
    def __init__(self, text):
        super().__init__()
        assert len(text) <= 4
        self.text = text

        for i, c in enumerate(self.text):
            if c == ' ':
                c = 'blue'

            signal = SIGNALS["signal-" + c]
            self.filters.append({
                "index": self.new_filter_index(),
                "signal": signal.get_json(),
                "count": 0,
            })
