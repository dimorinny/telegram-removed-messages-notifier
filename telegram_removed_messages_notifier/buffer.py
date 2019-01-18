from collections import OrderedDict


class CircularBufferDictionary(OrderedDict):
    def __init__(self, limit, *args, **kwargs):
        self._limit = limit
        OrderedDict.__init__(self, *args, **kwargs)
        self._check_size_limit()

    def __setitem__(self, key, value):
        OrderedDict.__setitem__(self, key, value)
        self._check_size_limit()

    def _check_size_limit(self):
        if self._limit is not None:
            while len(self) > self._limit:
                self.popitem(last=False)
