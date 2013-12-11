Quintagroup robotframework utils
=====================================

Data file parser
----------------

Datafile library provides more convenient way to save some of your test
data than robotframework variables tables do.


For example you have a file 'users.rst' where you save users accounts information:

::

    **Accounts on site**

    =========  ====  ========  =================
    users      id    password  email
    =========  ====  ========  =================
    admin      Eric  passwr    eric@example.com
    manager    Jonh  passwr    jonh@example.com
    publisher  Olga  passwr    olga@example.com
    reader     Jane  passwr    _table_:
    \                          work; jane@work.com|
    \                          pesonal; jane@pesonal.com
    =========  ====  ========  =================




and in test case you can parse this file and access its data in the following manner:

::

    *** Settings ***
    Library         quintagroup.robotframework.datafile.rst

    *** Test Cases ***
    Attribute alike access
        ${users}=  Read tables from file  ${CURDIR}/users.rst
        Should Be Equal  ${users.admin.id}  Eric
        Should Be Equal  ${users.manager.email}  jonh@example.com
        Should Be Equal  ${users.reader.id}  Jane
        Should Be Equal As String  ${users.reader.email}  [['work', 'jane@work.com'], ['pesonal', 'jane@pesonal.com']]
        Should Be Equal As String  ${users.reader.email}[0]  ['work', 'jane@work.com']

