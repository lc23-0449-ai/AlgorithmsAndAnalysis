from doubly_linked import DoublyLinkedList


def test_adds_front():
    ls = DoublyLinkedList()
    ls.add_front(1)
    ls.add_front(2)
    ls.add_front(3)
    assert str(ls) == '<3, 2, 1>'


def test_adds_back():
    ls = DoublyLinkedList()
    ls.add_back(1)
    ls.add_back(2)
    ls.add_back(3)
    assert str(ls) == '<1, 2, 3>'


def test_removes_front():
    ls = DoublyLinkedList()
    ls.add_back(1)
    ls.add_back(2)
    ls.add_back(3)
    ls.remove_front()
    assert str(ls) == '<2, 3>'
    ls.remove_front()
    assert str(ls) == '<3>'
    ls.remove_front()
    assert str(ls) == '<>'


def test_removes_back():
    ls = DoublyLinkedList()
    ls.add_front(3)
    ls.add_front(2)
    ls.add_front(1)
    ls.remove_back()
    assert str(ls) == '<1, 2>'
    ls.remove_back()
    assert str(ls) == '<1>'
    ls.remove_back()
    assert str(ls) == '<>'


def test_concatenates():
    a = DoublyLinkedList()
    a.add_back(1)
    a.add_back(2)
    a.add_back(3)
    b = DoublyLinkedList()
    b.add_back(4)
    b.add_back(5)
    b.add_back(6)
    a.concatenate(b)
    assert str(a) == '<1, 2, 3, 4, 5, 6>'


def test_removals_do_not_break_concatenation():
    a = DoublyLinkedList()
    b = DoublyLinkedList()
    for i in range(4):
        a.add_back(i)
        b.add_back(i + 4)
    a.remove_back()
    a.remove_front()
    b.remove_front()
    b.remove_back()
    a.concatenate(b)
    assert str(a) == '<1, 2, 5, 6>'
