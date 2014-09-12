#!/usr/bin/env python3

import unittest

import lazylist

class TestGetItem(unittest.TestCase):
    def test_incremental(self):
        range_size = 10
        lazy = lazylist.List(range(range_size))
        for i in range(range_size):
            lazy[i]
            self.assertEqual(len(lazy._list), i + 1)
        self.assertEqual(len(lazy), range_size)
        for a, b in zip(lazy._list, range(range_size)):
            self.assertEqual(a, b)
            

    def test_all_at_once(self):
        range_size = 10
        lazy = lazylist.List(range(range_size))
        lazy[range_size - 1]
        self.assertEqual(len(lazy._list), range_size)

    def test_negative_index(self):
        range_size = 10
        lazy = lazylist.List(range(range_size))
        for i in range(range_size):
            self.assertEqual(lazy[-(i + 1)], range_size - i - 1)


class TestSetItem(unittest.TestCase):
    def test_zero_out(self):
        range_size = 10
        lazy = lazylist.List(range(range_size))
        for i in range(range_size):
            lazy[i] = 0
        for i in range(range_size):
            self.assertEqual(lazy[i], 0)


class TestDelItem(unittest.TestCase):
    def test_remove_middle(self):
        range_size = 10
        lazy = lazylist.List(range(range_size))
        del lazy[4]
        self.assertEqual(lazy[3] + 2, lazy[4])


class TestLen(unittest.TestCase):
    def test_lens(self):
        seq = list(range(10))
        self.assertEqual(len(seq), len(lazylist.List(seq)))


class TestContains(unittest.TestCase):
    def test_range(self):
        range_min = 10
        range_max = 20
        lazy = lazylist.List(range(range_min, range_max))
        for i in range(range_min, range_max):
            self.assertTrue(i in lazy)
        for i in range(0, range_min):
            self.assertFalse(i in lazy)
        for i in range(range_max, range_max + 10):
            self.assertFalse(i in lazy)

class TestBool(unittest.TestCase):
    def test_for_false(self):
        self.assertFalse(lazylist.List(range(0)))
        self.assertFalse(lazylist.List([]))

    def test_for_true(self):
        self.assertTrue(lazylist.List(range(1)))
        self.assertTrue(lazylist.List([1]))

class TestExtend(unittest.TestCase):
    def test_two_range(self):
        lazy = lazylist.List(range(10))
        lazy[3]
        lazy.extend(range(10, 20))
        for i in range(20):
            self.assertEqual(lazy[i], i)

    def test_iadd(self):
        lazy = lazylist.List(range(10))
        lazy[3]
        lazy += range(10, 20)
        for i in range(20):
            self.assertEqual(lazy[i], i)

class TestRepr(unittest.TestCase):
    def test_simple(self):
        lazy = lazylist.List(range(3))
        self.assertEqual(repr(lazy), '[0, 1, 2]')

class TestEquality(unittest.TestCase):
    def test_should_equal(self):
        a = lazylist.List(range(3))
        b = lazylist.List(range(3))
        self.assertTrue(a == b)
        self.assertFalse(a != b)

    def test_totally_different(self):
        a = lazylist.List(range(3))
        b = lazylist.List(range(3, 10))
        self.assertFalse(a == b)
        self.assertEqual(len(a._list), 1)
        self.assertEqual(len(b._list), 1)
        self.assertTrue(a != b)

    def test_different_length(self):
        range_size = 10
        a = lazylist.List(range(range_size))
        b = lazylist.List(range(range_size + 1))
        self.assertFalse(a == b)
        self.assertTrue(a != b)


if __name__ == '__main__':
    unittest.main()
