from index_min_pq import IndexMinPQ
import string
import random


def test_recovers_one_item():
    q = IndexMinPQ()
    q.enqueue('a', 1)
    assert q.dequeue() == 'a'


def test_detects_emptiness():
    q = IndexMinPQ()
    assert q.is_empty()
    q.enqueue('a', 1)
    assert not q.is_empty()
    q.dequeue()
    assert q.is_empty()


def test_recovers_items_in_priority_order():
    q = IndexMinPQ()
    pairs = [(random.random(), letter) for letter in string.ascii_lowercase]
    for priority, key in pairs:
        q.enqueue(key, priority)
    out = []
    while not q.is_empty():
        out.append(q.dequeue())
    assert out == [k for p, k in sorted(pairs)]


def test_reduces_priority():
    q = IndexMinPQ()
    pairs = [(random.random(), letter) for letter in string.ascii_lowercase]
    for priority, key in pairs:
        q.enqueue(key, priority)
    pairs[0] = (-2, 'a')
    pairs[1] = (-1, 'b')
    q.reduce_priority('a', -2)
    q.reduce_priority('b', -1)
    out = []
    while not q.is_empty():
        out.append(q.dequeue())
    assert out == [k for p, k in sorted(pairs)]
