import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "DateRangeParser",
    packages = ['daterangeparser'],
    requires = ['pyparsing'],
    version = "0.1",
    author = "Robin Wilson",
    author_email = "robin@rtwilson.com",
    description = ("""Module to parse human-style date ranges (eg. 15th-19th March 2011) to datetimes"""),
    license = "LGPL",
    url = "http://packages.python.org/DateRangeParse",
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
        "Programming Language :: Python"
        
    ],
)