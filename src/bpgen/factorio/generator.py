import os

OUTPUT_PATH = os.path.join('factorio', 'generated')
DATA_PATH = os.path.join('factorio', 'data')


class SignalsGenerator:
    def __init__(self, output_path):
        self.output_path = output_path

        # List of string
        self.item_signals = []
        self.virtual_signals = []

        self.gathering_data()

        self.item_signals.sort()

    def _get_name_lua_line(self, line):
        return line.split('"')[1]

    def gathering_data(self):
        with open(os.path.join(DATA_PATH, 'item.lua')) as f:
            for line in f.readlines()[98:]:
                if line.startswith('    name ='):
                    name = self._get_name_lua_line(line)

                    # Drop that
                    if name == 'loader':
                        continue

                    self.item_signals.append(name)

        with open(os.path.join(DATA_PATH, 'signal.lua')) as f:
            for line in f.readlines()[1:]:
                if 'name' in line:
                    name = self._get_name_lua_line(line)

                    self.virtual_signals.append(name)

    def generate(self):
        output = ''
        output += 'from bpgen.factorio.signal import *\n'
        output += '\n'

        for name in self.item_signals:
            py_name = name.upper().replace('-', '_')
            output += 'SIGNAL_{} = ItemSignal("{}")\n'.format(py_name, name)

        output += '\n'

        for name in self.virtual_signals:
            py_name = name.upper().replace('-', '_')
            output += '{} = VirtualSignal("{}")\n'.format(py_name, name)

        output += '\n'

        output += 'SIGNALS = {\n'
        for name in self.item_signals + self.virtual_signals:
            py_name = name.upper().replace('-', '_')

            if not py_name.startswith('SIGNAL_'):
                py_name = 'SIGNAL_' + py_name

            output += '    "{}": {},\n'.format(name, py_name)
        output += '}\n'

        output += '\n'

        with open(self.output_path, 'w') as f:
            f.write(output)


def main():
    generator = SignalsGenerator(os.path.join(OUTPUT_PATH, 'signals.py'))
    generator.generate()


if __name__ == '__main__':
    main()
