"""iterlist is a list-like interface for iterables."""
# pylint: disable=C0103,R0205

try:
    from collections.abc import Sequence
except ImportError:
    # python 2 compatible
    from collections import Sequence
import itertools
izip = getattr(itertools, "izip", zip)  # python2 compatible iter zip
try:
    from typing import Any, Callable, Iterable, Iterator, List, Optional, Union
except ImportError:
    pass  # typing is only used for static analysis


class IterList(object):
    """a list-like interface over an iterable that stores iterated values."""

    def __init__(self, iterable):
        # type: (Iterable) -> None
        """Initialize

        :type iterable: Iterable
        """
        self._iterable = iter(iterable)
        self._list = list()  # type: List[Any]

    def _positive_index(self, index):
        # type: (int) -> int
        """Private

        If index is positive, it is returned.
        If index is negative, it is converted to a positive index referring to
        the same position

        :rtype: int
        :return: positive list index for index
        :raise: IndexError if the magnitude of index is greater than the length
                of the iterable
        """
        if index >= 0:
            return index
        self._consume_rest()
        pos = len(self._list) - abs(index)
        if pos < 0:
            raise IndexError('list index out of range')
        return pos

    def _consume_next(self):
        # type: () -> None
        exhausted = False
        try:
            self._list.append(next(self._iterable))
        except StopIteration:
            exhausted = True
        if exhausted:
            raise IndexError

    def _consume_rest(self):
        # type: () -> None
        self._list.extend(self._iterable)

    def _consume_up_to_index(self, index):
        # type: (int) -> None
        if index < 0:
            self._consume_rest()
            return
        to_consume = index - len(self._list) + 1
        for _ in range(to_consume):
            self._consume_next()

    def _consume_up_to_slice(self, sl):
        # type: (slice) -> None
        consume_to = None
        start, stop, step = sl.start, sl.stop, sl.step
        if start is None:
            start = 0
        if stop is None:
            stop = 0
        if step is None:
            step = 1

        if sl.start is None and sl.stop is None:
            # full slice
            consume_to = -1
        elif start < 0 or stop < 0:
            # negative slice, must consume the whole iterator
            consume_to = min(start, stop)
        elif step > 0 and sl.stop is None:
            # positive slice, no end specified
            consume_to = -1
        elif step > 0 and stop > start:
            # positive slice
            consume_to = stop - ((stop - start) % step) - 1
        elif step < 0 and stop < start:
            # reversed slice will always include the item at index start
            consume_to = start
        else:
            # empty slice, nothing to consume
            pass
        self._consume_up_to(consume_to)

    def _consume_up_to(self, key):
        # type: (Optional[Union[slice, int]]) -> None
        if key is None:
            return
        if isinstance(key, slice):
            self._consume_up_to_slice(key)
        else:
            self._consume_up_to_index(key)

    def __getitem__(self, index):
        # type: (Union[slice, int]) -> Any
        self._consume_up_to(index)
        return self._list[index]

    def __setitem__(self, index, value):
        # type: (Union[slice, int], Any) -> None
        self._consume_up_to(index)
        self._list[index] = value

    def __delitem__(self, index):
        # type: (Union[slice, int]) -> None
        self._consume_up_to(index)
        del self._list[index]

    def __len__(self):
        # type: () -> int
        self._consume_rest()
        return len(self._list)

    def __bool__(self):
        # type: () -> bool
        if self._list:
            return True
        try:
            self._consume_next()
            return True
        except IndexError:
            return False

    __nonzero__ = __bool__

    def extend(self, rest):
        # type: (Iterable) -> None
        """Extend the list with an iterable."""
        self._iterable = itertools.chain(self._iterable, iter(rest))

    def __iadd__(self, rest):
        # type: (Iterable) -> IterList
        self.extend(rest)
        return self

    def __repr__(self):
        # type: () -> str
        self._consume_rest()
        return '[' + ', '.join(repr(item) for item in self._list) + ']'

    def __eq__(self, other):
        # type: (Any) -> bool
        if not isinstance(other, (IterList, Sequence)):
            return False
        return (all(a == b for a, b in izip(self, other))
                and len(self) == len(other))

    def __ne__(self, other):
        # type: (Any) -> bool
        # python 2 requires __ne__ or assumes no object is equal
        return not self == other

    def __lt__(self, other):
        # type: (Any) -> bool
        for a, b in izip(self, other):
            if b < a:
                return False
            if a < b:
                return True

        # at this point all elements in both lists are equal
        # in this case, the shorter list is considered less
        try:
            self._consume_next()
        except IndexError:
            pass
        try:
            other._consume_next()
        except IndexError:
            pass
        return len(self._list) < len(other._list)

    def sort(self, key=None, reverse=False):
        # type: (Optional[Callable[[Any], bool]], bool) -> None
        """Stable sort in-place.

        Note: this will consume the entire iterable
        """
        self._consume_rest()
        self._list.sort(key=key, reverse=reverse)

    def reverse(self):
        # type: () -> None
        """Reverse in-place.

        Note: this will consume the entire iterable
        """
        self._consume_rest()
        self._list.reverse()

    def pop(self, index=-1):
        # type: (int) -> Any
        """Remove and return item at index (default last).

        Raises IndexError if list is empty or index is out of range.
        """
        self._consume_up_to(index)
        item = self._list[index]
        del self._list[index]
        return item

    def index(self, item, start=0, stop=None):
        # type: (Any, int, Optional[int]) -> int
        """Return first index of item.

        Raises ValueError if the value is not present.
        """
        start = self._positive_index(start)
        if stop:
            stop = self._positive_index(stop)
        for i, e in enumerate(itertools.islice(self, start, stop)):
            if e == item:
                return i + start

        raise ValueError('{} is not in list'.format(item))

    def count(self, item):
        # type: (Any) -> int
        """Return number of occurrences of item.

        Note: this will consume the entire iterable
        """
        self._consume_rest()
        return self._list.count(item)

    def remove(self, item):
        # type: (Any) -> None
        """Remove first occurrence of item.

        Raises ValueError if the value is not present.
        """
        del self[self.index(item)]

    def insert(self, index, item):
        # type: (int, Any) -> None
        """Insert item before index."""
        self._consume_up_to(index)
        self._list.insert(index, item)

    def append(self, item):
        # type: (Any) -> None
        """Append item to end.

        Note: this will consume the entire iterable
        """
        self._consume_rest()
        self._list.append(item)

    def clear(self):
        # type: () -> None
        """Clear the list

        Any unevaluated parts of the list will not be evaluated. This
        behavior may produce unexpected results if the evaluation of
        the remaining items has side effects.
        """
        del self._list[:]  # self._list.clear() for py3.3+
        self._iterable = iter([])

    def __iter__(self):
        # type: () -> Iterator[Any]
        ix = 0
        try:
            # Use a while loop over the list index to ensure all items are
            # yielded, even if some of the iterable is consumed while __iter__
            # is stopped
            while True:
                self._consume_up_to_index(ix)
                yield self._list[ix]
                ix += 1
        except IndexError:
            return
