from bubble import bubble_sort
import random


def test_sorts():
    for n in [0, 1, 2, 4, 10, 1000]:  # Different list lengths
        a = [random.random() for _ in range(n)]
        correct = sorted(a)
        bubble_sort(a)
        assert a == correct
