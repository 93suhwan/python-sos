from collections import OrderedDict


class Memory:
    """Memory is a finite mapping from locations to Num instances"""
    def __init__(self):
        self._store = OrderedDict()

    def __str__(self):
        h = 'Runtime Memory State'
        lines = [h, '=' * len(h)]
        for var, num in self._store.items():
            lines.append('%7s -> %r' % (var, num.value))

        s = '\n'.join(lines)
        return '\n' + s + '\n'

    __repr__ = __str__

    def insert(self, location, value):
        name = location.value
        self._store[name] = value

    def lookup(self, location):
        name = location.value
        value = self._store.get(name)
        if value is None:
            raise Exception('Undeclared variable %s' % name)
        return value
