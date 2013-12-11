"""
Datafile library provides more convenient way to save test data
than robotframework variables tables
"""

import re
from itertools import imap, ifilter
from quintagroup.robotframework.utils import bunchify

LAYOUT_RE = re.compile('^=+  +[=+|  +]*$')


def get_symbol_positions(line, character):
    """returns all symbols positions
    >>> st = '=========================  ========================' \
             '   ====================  ======='
    >>> get_symbol_positions(st, ' ')
    [25, 26, 51, 52, 53, 74, 75]
    """
    return [m.start() for m in re.finditer(character, line)]


def get_symbol_groups(line, character):
    """returns grouped symbols positions
    >>> st = '=========================  ========================' \
              '   ====================  ======='
    >>> get_symbol_groups(st, '=')
    [(0, 25), (27, 51), (54, 74), (76, None)]
    >>> st2 = '=================================='\
              '  =================================='
    >>> get_symbol_groups(st2, '=')
    [(0, 34), (36, None)]
    """
    pos = get_symbol_positions(line, character)
    # gets character (start,end) coordinates in lines
    anomals = sum([[i + 1, j] for i, j
                   in zip(pos[:-1], pos[1:]) if j - i - 1], [])
    anomals = [0] + anomals + [None]
    return zip(anomals[::2], anomals[1::2])


def is_table_markup_valid(lines):
    """checks table separators
    >>> valid = ['==  ==  ==', \
                 'a   b   cd', \
                 '==  ==  ==', \
                 'aa  bb  ddd', \
                 'aa',           \
                 '==  ==  ==']
    >>> is_table_markup_valid(valid)
    True
    >>> invalid = ['==  ==  ==', \
                   'a   b   cd', \
                   '==  ==  ==', \
                   'aa  bbc',     \
                   'aaf bb  ddd', \
                   '==  ==  ==']
    >>> is_table_markup_valid(invalid)
    False
    """
    separators_pos = get_symbol_positions(lines[0], ' ')
    for line in lines[1:]:
        for pos in separators_pos:
            if len(line) <= pos:
                break
            if line[pos] != ' ':
                return False
    return True


def split_by_empty_row(data):
    """ Splits text into blocks by empty lines
    >>> text = 'block1\\n' \
               '\\n' \
               'block2\\n' \
               'block2\\n' \
               '\\n ' \
               '         \\n' \
               'block3\\n' \
               '\\n'
    >>> split_by_empty_row(text)
    [['block1'], ['block2', 'block2'], ['block3']]
    """
    data = (row.rstrip(" ") for row in data.split("\n"))
    text_groups = [[], ]
    for row in data:
        if not row:
            text_groups.append([])
            continue
        text_groups[-1].append(row)
    return [i for i in text_groups if i]


def is_table_a_valid(data):
    """ checks markup rules for table
    >>> valid = ['==  ==  ==', \
                 'a   b   cd', \
                 '==  ==  ==', \
                 'aa  bb  ddd', \
                 '==  ==  ==']
    >>> is_table_a_valid(valid)
    True
    >>> invalid1 = ['== == ==', \
                    'a  b  cd', \
                    '== == ==', \
                    'aa bb dd', \
                    '== == ==']
    >>> is_table_a_valid(invalid1)
    False
    >>> invalid2 = ['==  ==  ==', \
                    'a   b   cd', \
                    'a   b   cd', \
                    '==  ==  ==', \
                    'aa  bb  dd', \
                    '==  ==  ==']
    >>> is_table_a_valid(invalid2)
    False
    >>> invalid3 = ['==  ==  ==', \
                    'a 1 b   cd', \
                    'a   b   cd', \
                    '==  ==  ==', \
                    'aa  bb  dd', \
                    '==  ==  ==']
    >>> is_table_a_valid(invalid3)
    False
    """
    return LAYOUT_RE.match(data[0]) and \
        len(set([data[0], data[2], data[-1]])) == 1 and \
        is_table_markup_valid(data) or False


def search_tables(data):
    """ Searches for valid tables
    >>> from pprint import pprint
    >>> from quintagroup.robotframework.utils.tests import TESTFILE
    >>> pprint(list(search_tables(TESTFILE)))
    [['==================================  =========================',
      'value_table                         value',
      '==================================  =========================',
      'key1                                value1',
      'key2                                value2',
      '==================================  ========================='],
     ['==============  ========================   ========  =======',
      'dicttable                  k1              k2             k3',
      '==============  ========================   ========  =======',
      'd1                   d1k1                  d1k2      something long',
      'd2              d2k1',
      'd3              d3k3                                 d3k3',
      'd4              d4k1dddddddddddddddddddd',
      'd5              d5k1                                 d5k3',
      '\\\\               k12                                  d5k32',
      '\\\\               k13',
      '==============  ========================   ========  =======']]
    """
    tables = ifilter(is_table_a_valid, split_by_empty_row(data))
    return tables


class RowDataReader():
    """ Table data parser

    >>> rd = RowDataReader([[1,2], [5,8]])
    >>> rd('0123456789')
    ['1', '567']

    """
    def __init__(self, layout):
        self.layout = layout

    def __call__(self, row):
        return [row[i[0]:i[1]].strip(" ") or None for i in self.layout]


def packing_data(keys, data):
    """ returns dict or value
    >>> packing_data(['a','b'],['c','d'])
    {'a': 'c', 'b': 'd'}
    >>> packing_data(['value'],['3'])
    '3'
    """
    if len(keys) == 1 and keys[0] == 'value':
        return data[0]
    return dict(zip(keys, data))


def pasre_tables(data):
    """ Transforms simple REST notation tables into the dictionaries
    >>> from pprint import pprint
    >>> from quintagroup.robotframework.utils.tests import TESTFILE
    >>> pprint(pasre_tables(TESTFILE), width=40)
    {'dicttable': {'d1': {'k1': 'd1k1',
                          'k2': 'd1k2',
                          'k3': 'something long'},
                   'd2': {'k1': 'd2k1',
                          'k2': None,
                          'k3': None},
                   'd3': {'k1': 'd3k3',
                          'k2': None,
                          'k3': 'd3k3'},
                   'd4': {'k1': 'd4k1dddddddddddddddddddd',
                          'k2': None,
                          'k3': None},
                   'd5': {'k1': 'd5k1k12k13',
                          'k2': None,
                          'k3': 'd5k3d5k32'}},
     'value_table': {'key1': 'value1',
                     'key2': 'value2'}}
    """
    raw_tables = search_tables(data)
    tables = {}
    for table in raw_tables:
        data_reader = RowDataReader(get_symbol_groups(table[0], '='))
        keys = data_reader(table[1])
        data = imap(data_reader, table[3:-1])
        # merge escaped rows with upper row
        merged_data = []
        for row in data:
            if row[0][0] == '\\':
                row[0] = row[0][1:]
                for n, i in enumerate(row):
                    if merged_data[-1][n] and i:
                        merged_data[-1][n] += i
                continue
            merged_data.append(row)

        tables[keys[0]] = dict([(i[0], packing_data(keys[1:], i[1:]))
                                for i in merged_data])
    return tables


def replace_patterns(dict_structure):
    """ replaces patterns in dict objects
    >>> replace_patterns({'dicttable': {'d1': {'k1': '_table_:a; 1 | b; 2 | c; 3',}}})
    {'dicttable': {'d1': {'k1': [['a', '1'], ['b', '2'], ['c', '3']]}}}

    """
    for key, value in dict_structure.items():
        if isinstance(value, dict):
            dict_structure[key] = replace_patterns(value)
        else:
            if not value:
                continue
            if value.startswith('_table_:'):
                dict_structure[key] = [[i.strip() for i in row.split(";")]
                                       for row in value.split(":")[1].split("|")]
    return dict_structure


def read_tables_from_file(data_file):
    """
    Transforms file data to dictionary objects.
    This function works with rest files, but also can work with html.

    >>> from os import path
    >>> here = path.dirname(path.abspath(__file__))
    >>> data = read_tables_from_file(path.join(here, 'test.rst'))
    >>> data.users.admin.id
    'Eric'
    >>> data.users.publisher.email
    'olga@example.com'
    >>> data.users.publisher.Full_name

    >>> data.site_navigation.home_page
    'http://example.com'

    """
    data = open(data_file).read()
    tables = pasre_tables(data)
    return bunchify(replace_patterns(tables))
