DateRangeParser Documentation
===========================================

Introduction
------------
DateRangeParser is a Python module which makes it easy to parse human-style date ranges like "4-8th May" or "Wed 19th June - Thurs 30th August 2014". It is very simple, consisting of one `parse` method which does the parsing.

Installation
------------
DateRangeParser can be installed from the Python Package Index by running::

  pip install daterangeparser
  
DateRangeParser is built upon `PyParsing <http://pyparsing.wikispaces.com/>`_, and requires the PyParsing module to be installed for it to work correctly. The command above should install PyParsing if it is not currently installed.

Quickstart
----------

Using DateRangeParser is very easy - simply follow the steps below.

1. Import the parse function::

    from daterangeparser import parse

2. Run the parse function on a string::

    start, end = parse("3rd May-18th July 2014")
  
3. Use the results somehow::

    print "Start = %s" % start
    print "End = %s" % end
    print "Days between start and end = %i" % (end-start).days
    
4. That's it! Simple, isn't it.

What formats will this work with?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Most date range formats that use specific dates (rather than 'tomorrow' or 'last wednesday') should work fine. Examples that are known to work include:

- 27th-29th June 2010
- 30 May - 9th Aug
- 3rd Jan 1980 - 2nd Jan 2013
- Wed 23 Jan - Sat 16 February 2013
- Tue 29 May - Sat 2 June 2012
- 1-9 Jul