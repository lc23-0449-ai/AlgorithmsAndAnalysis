from horspool import HorspoolStringMatcher


def test_computes_correct_shift_table():
    matcher = HorspoolStringMatcher('mississippi')
    assert matcher._get_shift('m') == 10
    assert matcher._get_shift('i') == 3
    assert matcher._get_shift('s') == 4
    assert matcher._get_shift('p') == 1
    assert matcher._get_shift('a') == 11


def test_finds_early_match():
    matcher = HorspoolStringMatcher('How')
    assert matcher.match('How much wood would a woodchuck chuck if a woodchuck could chuck wood?') == 0


def test_finds_middle_match():
    matcher = HorspoolStringMatcher('woodchuck')
    assert matcher.match('How much wood would a woodchuck chuck if a woodchuck could chuck wood?') == 22


def test_finds_late_match():
    matcher = HorspoolStringMatcher('wood?')
    assert matcher.match('How much wood would a woodchuck chuck if a woodchuck could chuck wood?') == 65


def test_detects_nonmatch():
    matcher = HorspoolStringMatcher('plastic')
    assert matcher.match('How much wood would a woodchuck chuck if a woodchuck could chuck wood?') == -1


def test_does_not_contain_common_bug_1():
    matcher = HorspoolStringMatcher('aabab')
    assert matcher.match('xxxaabab') == 3


def test_does_not_contain_common_bug_2():
    matcher = HorspoolStringMatcher('abba')
    assert matcher.match('cccbabba') == 4
