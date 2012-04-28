import os
from setuptools import setup


setup(
    name = "DateRangeParser",
    packages = ['daterangeparser'],
    install_requires = ['pyparsing'],
    version = "0.3",
    author = "Robin Wilson",
    author_email = "robin@rtwilson.com",
    description = ("""Module to parse human-style date ranges (eg. 15th-19th March 2011) to datetimes"""),
    license = "LGPL",
    url = "https://github.com/robintw/daterangeparser",
    long_description="""DateRangeParser is a Python module which makes it easy to parse date ranges specified in
    a human-style string. For example, it can parse strings like:
    
      - 27th-29th June 2010
      - 30 May - 9th Aug
      - 3rd Jan 1980 - 2nd Jan 2013
      - Wed 23 Jan - Sat 16 February 2013
      - Tuesday 29 May - Sat 2 June 2012
      - 1-9 Jul
    
    Full documentation is provided at http://daterangeparser.readthedocs.org/ and the code (and development information)
    is available at https://github.com/robintw/daterangeparser.""",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
        "Programming Language :: Python"
        
    ],
)