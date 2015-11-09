DateRangeParser Documentation
===========================================

Introduction
------------
DateRangeParser is a Python module which makes it easy to parse human-style date ranges like "4-8th May" or "Wed 19th June - Thurs 30th August 2014". It is very simple, consisting of one `parse` method which does the parsing.

This module is released under the GNU Lesser General Public License - see the COPYING and COPYING.LESSER files in the source directory for details.

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
Most date range formats that use specific dates (rather than 'tomorrow' or 'last wednesday') should work fine. The parser works for date ranges and single dates (in this case returning a start date and `None` for the end date), and ignores any time details that are in the strings.

Examples that are known to work include:

- 27th-29th June 2010
- January 10th - 11th
- 30 May to 9th Aug
- 3rd Jan 1980 -- 2nd Jan 2013
- Wed 23 Jan -> Sat 16 February 2013
- Tuesday 29 May - Sat 2 June 2012
- From 1 to 9 Jul
- 14th July 1988
- July 14th 1988
- 1988 14th July
- Nov 18th - 23rd Dec
- 07:00 Tue 7th June - 17th July 3:30pm
- Jan - Mar (gives dates from the first day in the first month to the last day in the second month, taking into account leap years)

More details are available in the function documentation below.

Function Documentation
^^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: daterangeparser.parse

Release Notes
-------------

1.2
^^^
Now works on both Python 2 and Python 3

Modified so that the start month is used if the end month doesn't exist (so something like "Jan 10th-11th" will now work)

1.1.1
^^^^^
Modified so that "July" now produces a range from the 1st to the 31st July.

Added ranges based only on years, so "2013" produces a range from 1st Jan 2013 to the 31st Dec 2013, and similarly
for "1995-2010".

1.0
^^^
Added ability to parse dates with no days specified - they will default to the first or last day of the month.

For example:

"Sep 2011 - Nov 2013" will produce 01/09/2011 to 30/11/2013

This also works with single dates:

"July" will produce 01/07/XXXX (where XXXX is the current year)

Fixed minor bugs, and bumped to stable release of version 1.0

0.6
^^^
First release with main functionality.
