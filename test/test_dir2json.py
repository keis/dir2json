from hamcrest import assert_that, has_entry, empty, only_contains
import dir2json


def test_index_empty_directory():
    target = 'foo/'
    scanner = [(target, [], [])]

    index = dir2json.create_index(target, scanner)

    assert_that(index, has_entry('type', 'directory'))
    assert_that(index, has_entry('index', empty()))


def test_index_some_files():
    target = 'foo/'
    scanner = [(target, [], ['zoidberg.txt', 'rick.py'])]

    index = dir2json.create_index(target, scanner)

    assert_that(index, has_entry('type', 'directory'))
    assert_that(index, has_entry('index',
                                 only_contains({'path': 'rick.py',
                                                'type': 'text/x-python'},
                                               {'path': 'zoidberg.txt',
                                                'type': 'text/plain'})))


def test_index_some_directories():
    target = 'foo/'
    scanner = [(target, ['one', 'two'], []),
               (target + 'one', [], ['zoidberg.txt']),
               (target + 'two', [], ['zoidberg.txt'])]

    index = dir2json.create_index(target, scanner)

    dirone = has_entry('index',
                       only_contains(has_entry('path', 'one/zoidberg.txt')))
    dirtwo = has_entry('index',
                       only_contains(has_entry('path', 'two/zoidberg.txt')))

    assert_that(index, has_entry('type', 'directory'))
    assert_that(index, has_entry('index', only_contains(dirone, dirtwo)))


def test_index_nested():
    target = 'foo/'
    scanner = [(target, ['one'], []),
               (target + 'one', ['two'], []),
               (target + 'one/two', [], ['zoidberg.txt'])]

    index = dir2json.create_index(target, scanner)
    deep = index['index'][0]['index'][0]['index']
    assert_that(deep, only_contains(has_entry('path',
                                              'one/two/zoidberg.txt')))
