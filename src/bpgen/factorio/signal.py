class Signal:
    def __init__(self, type_, name):
        self.type = type_
        self.name = name

    def get_json(self):
        return {
            "type": self.type,
            "name": self.name,
        }


class ItemSignal(Signal):
    def __init__(self, name):
        super().__init__("item", name)


class VirtualSignal(Signal):
    def __init__(self, name):
        super().__init__("virtual", name)
