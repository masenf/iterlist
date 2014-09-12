import itertools

class List:
    def __init__(self, iterable):
        self._iterable = iter(iterable)
        self._list = list()

    @property
    def _exhausted(self):
        try:
            self._consume_next()
            return False
        except IndexError:
            return True

    def _consume_next(self):
        exhausted = False
        try:
            self._list.append(next(self._iterable))
        except StopIteration:
            exhausted = True
        if exhausted:
            raise IndexError

    def _consume_rest(self):
        self._list.extend(self._iterable)

    def _consume_up_to_value(self, value):
        if value < 0:
            self._consume_rest()
            return
        to_consume = value - len(self._list) + 1
        for i in range(to_consume):
            self._consume_next()
    
    def _slice_max(self, sl):
        start, stop, step = sl.start, sl.stop, sl.step
        if step == None:
            step = 1
        if step > 0 and stop > start:
            return stop - ((stop - start) % step)
        elif step < 0 and stop < start:
            return stop + ((start - stop) % (-step))
        else:
            return 0

    def _consume_up_to_slice(self, sl):
        if sl.start < 0 or sl.stop < 0:
            self._consume_rest()
        else:
            self._consume_up_to(self._slice_max(sl))

    def _consume_up_to(self, index):
        if isinstance(index, slice):
            self._consume_up_to_slice(index)
        else:
            self._consume_up_to_value(index)

    def __getitem__(self, index):
        self._consume_up_to(index)
        return self._list[index]

    def __setitem__(self, index, value):
        self._consume_up_to(index)
        self._list[index] = value

    def __delitem__(self, index):
        self._consume_up_to(index)
        del self._list[index]
        
    def __len__(self):
        self._consume_rest()
        return len(self._list)

    def __bool__(self):
        if self._list:
            return True
        try:
            self._consume_next()
            return True
        except IndexError:
            return False

    def extend(self, rest):
        self._iterable = itertools.chain(self._iterable, iter(rest))

    def __iadd__(self, rest):
        self.extend(rest)
        return self
    
    def __repr__(self):
        self._consume_rest()
        return '[' + ', '.join(repr(item) for item in self._list) + ']'

    def __eq__(self, other):
        return (all(a == b for a, b in zip(self, other))
                and self._exhausted
                and other._exhausted
                and len(self) == len(other))
