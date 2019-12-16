# iterlist

Lazily evaluated lists in Python

An `iterlist.IterList` accepts a single iterable as its only constructor argument.

The `iterlist.IterList` behaves as a normal list, and will only
evaluate the iterable as needed to satisfy requests for element.

If there is a request for index `[5]`, then elements 0 - 5 will be
evaluated if they have not been yet. Certain operations like `len` and
negative indexing will force the list to be evaluated. This decision was made
to make the iterlist outwardly appear as much like a normal list as possible.

## Infinite Iterators

This implementation does not make any attempt to protect you from running out
of memory attempting to construct a list from an infinite iterator. A future
version may implement `InfiniteIterList`, which will not have support for any
operation which would require consuming the entire iterable.

# License

BSD 2-clause (inherited from lazylist)

# Prior Work

Apparently this is not a new idea...

Forked from: https://github.com/ryanhaining/lazylist (2014/10)

http://stupidpythonideas.blogspot.com/2014/07/lazy-python-lists.html (2014/07)

http://code.activestate.com/recipes/576410-lazy-lists/ (2008/08)

http://www.logarithmic.net/pfh/blog/01193268742 (unknown)
