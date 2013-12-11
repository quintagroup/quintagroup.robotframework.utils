"""
Bunch is a dictionary that supports attribute-style access. The only
difference with Bunch(look at https://github.com/dsc/bunch) is that
this library normalizes keys into attribute style notation.
    >>> a = {'a': 1}
    >>> a['a']
    1
    >>> b = bunchify(a)
    >>> b.a
    1
"""

import re
import bunch as _bunch

NOT_ALLOWED_CHARACTERS = re.compile(r'[ \-\$\%\(\)\/\*\{\}\[\]!\+,\.]')


def properties_names_normalizer(dictionary):
    """transforms all dictionary keys into attribute style notation
    by replacing not allowed symbols with '_'
    >>> properties_names_normalizer({'a ': {'b!': {'c':{'d':{'e':{'f':1}}}}}})
    {'a': {'b_': {'c': {'d': {'e': {'f': 1}}}}}}
    >>> properties_names_normalizer({'k1':{'k2':{'k3':['hello ', 3], \
                         ' Abc.df. e-$%()/*{}[]+,end  ':1}}, \
                         'k4 and some spaces':5})
    {'k1': {'k2': {'k3': ['hello ', 3], 'Abc_df__e_____________end': 1}}, \
'k4_and_some_spaces': 5}
    """
    for key in dictionary:
        value = dictionary.pop(key)
        key = NOT_ALLOWED_CHARACTERS.sub('_', key.strip(" "))
        if isinstance(value, dict):
            dictionary[key] = properties_names_normalizer(value)
        else:
            dictionary[key] = value
    return dictionary


def bunchify(dictionary):
    """ builds class from dict where any value can be reached like a property
    >>> obj = bunchify({'k1':{'k2':{'k3':['hello ', 3], \
                        ' Abc.df. e-$%()/*{}[]+,end  ':1}}, \
                        'k4 and some spaces':5})
    >>> obj.k1.k2.k3
    ['hello ', 3]
    >>> obj.k4_and_some_spaces
    5
    >>> obj.k1.k2.Abc_df__e_____________end
    1
    """
    return _bunch.bunchify(properties_names_normalizer(dictionary))
