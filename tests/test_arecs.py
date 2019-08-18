from arecs.records import group, parse_ects


def test_parse_ects():
    assert (int(parse_ects('<!-- document.write(Math.round(12.0*10)/10); //-->'))) == 12


def test_group():
    lst = [1, 2, 3, 'a', 'b', 'c']
    res = [(1, 2, 3), ('a', 'b', 'c')]
    grp = list(group(lst, 3))
    assert (grp) == res
    assert isinstance(grp[0], tuple)

    lst = [1, 2, 3]
    assert (list(group(lst, 3))) == [(1, 2, 3)]

    lst = [1, 2, 3]
    assert (list(group(lst, 2))) == [(1, 2), (3,)]

    lst = []
    assert (list(group(lst, 1))) == []
