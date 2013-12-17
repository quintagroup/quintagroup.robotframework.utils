from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='quintagroup.robotframework.utils',
      version=version,
      description="Datafile library that provides more convenient way to save some of your test data than robotframework variables tables",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='robotframework',
      author='Quintagroup',
      author_email='support@quintagroup.com',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      extras_require={
          'tests': ['nose',
                    'nose-selecttests',]
      },
      namespace_packages=['quintagroup', 'quintagroup.robotframework'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'bunch',
          'python-dateutil',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
