TESTFILE = """

============  ========
bad table1     v
============  =======
k11            d11
============  =======

============  =======
bad table2    v
============  =======
k21         32 d21
============  =======


============  =======
bad table3     v
============= =======
k31            d31
============  =======

============   =======
bad table4    v
============   =======
k41            d41
============   =======

============   =======
bad table5     v
============   =======
k51       dsf  d51
============   =======


==================================  =========================
value_table                         value
==================================  =========================
key1                                value1
key2                                value2
==================================  =========================

some markup
=========  ===

some markup2
============

**Accounts on site**

==============  ========================   ========  =======
dicttable                  k1              k2             k3
==============  ========================   ========  =======
d1                   d1k1                  d1k2      something long
d2              d2k1
d3              d3k3                                 d3k3
d4              d4k1dddddddddddddddddddd
d5              d5k1                                 d5k3
\               k12                                  d5k32
\               k13
==============  ========================   ========  =======

"""
