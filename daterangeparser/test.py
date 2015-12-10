# daterangeparser - a Python library to parse string date ranges
# Copyright (C) 2013  Robin Wilson

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest
import datetime
from .parse_date_range import parse
from pyparsing import ParseException


class TestWorkingParsing(unittest.TestCase):
    tests = [
        # Various
        ("27th-29th June 2010", "27/06/2010", "29/06/2010"),
        ("30 May - 9th Aug", "30/05/XXXX", "9/8/XXXX"),
        ("3rd Jan 1980 - 2nd Jan 2013", "3/1/1980", "2/1/2013"),
        ("Wed 23 Jan - Sat 16 February 2013", "23/1/2013", "16/2/2013"),
        ("Tuesday 29 May - Sat 2 June 2012", "29/5/2012", "2/6/2012"),
        ("1-9 Jul", "1/7/XXXX", "9/7/XXXX"),
        ("Tuesday 19th June - Wednesday 20th June 2013", "19/6/2013", "20/6/2013"),
        ("January 10th - 11th", "10/1/XXXX", "11/1/XXXX"),

        # Different separators
        ("14--16th May", "14/5/XXXX", "16/5/XXXX"),
        ("14-16th May", "14/5/XXXX", "16/5/XXXX"),
        ("14 - 16th May", "14/5/XXXX", "16/5/XXXX"),
        ("14 -- 16th May", "14/5/XXXX", "16/5/XXXX"),
        ("14--16th May", "14/5/XXXX", "16/5/XXXX"),
        ("14 to 16th May", "14/5/XXXX", "16/5/XXXX"),
        ("14 until 16th May", "14/5/XXXX", "16/5/XXXX"),
        ("14 through 16th May", "14/5/XXXX", "16/5/XXXX"),
        ("14 \u2013 16th May", "14/5/XXXX", "16/5/XXXX"),
        ("14 \u2014 16th May", "14/5/XXXX", "16/5/XXXX"),
        ("14-> 16th May", "14/5/XXXX", "16/5/XXXX"),

        # Individual Dates
        ("14th July 1988", "14/7/1988", None),
        ("1 May 2000", "1/5/2000", None),
        ("7 June", "7/6/XXXX", None),
        ("Saturday 19th July 1935", "19/7/1935", None),
        ("Sat 6 Aug", "6/8/XXXX", None),
        ("2015 12 thursday November", "12/11/2015", None),

        # Ignorable characters
        ("14, July", "14/7/XXXX", None),
        ("From 1st to 9th Jan 2008", "1/1/2008", "9/1/2008"),
        ("beGinning 1st to 9th Sept 2008", "1/9/2008", "9/9/2008"),
        ("17th, -, 19th June 1987", "17/6/1987", "19/6/1987"),
        ("26-29 Oct. 2009", "26/10/2009", "29/10/2009"),
        ("15th of December", "15/12/XXXX", None),
        ("from 10th till 11th of April", "10/4/XXXX", "11/4/XXXX"),

        # Ignoring of times
        ("14th July 1988 06:45", "14/7/1988", None),
        ("14th July 1988 06.45am", "14/7/1988", None),
        ("14th July 1988 3:30pm", "14/7/1988", None),
        ("12:37 1st Jan - 17th Feb 19:00", "1/1/XXXX", "17/2/XXXX"),

        # Things in different orders
        ("July 14", "14/7/XXXX", None),
        ("1990, Dec 29 - 1992, Dec 14", "29/12/1990", "14/12/1992"),
        ("Thurs Nov 11th 1954", "11/11/1954", None),

        # Dates with no days
        ("July", "01/07/XXXX", "31/07/XXXX"),
        ("Feb 2010", "01/02/2010", "28/02/2010"),
        ("Feb 1996", "01/02/1996", "29/02/1996"),
        ("Feb to Nov", "01/02/XXXX", "30/11/XXXX"),
        ("Feb 2010 - Feb 2012", "01/02/2010", "29/02/2012"),

        # Bare year
        ("2013", "01/01/2013", "31/12/2013"),
        ("1995 - 2010", "01/01/1995", "31/12/2010"),

        # Straddling end of year
        ("25 Dec - 2 Jan 2016", "25/12/2015", "02/01/2016"),
        ("18 Nov 2015 to 14th Feb 2016", "18/11/2015", "14/02/2016"),
        ("18 Nov 2010 to 14th Feb 2016", "18/11/2010", "14/02/2016"),

        ("26-29 Oct. 2009", "26/10/2009", "29/10/2009")

    ]

    def runTest(self):
        for test in self.tests:
            text, start, end = test
            current_year = datetime.date.today().year
            start = start.replace("XXXX", str(current_year))
            start_dt = datetime.datetime.strptime(start, "%d/%m/%Y")

            if end is not None:
                end = end.replace("XXXX", str(current_year))
                end_dt = datetime.datetime.strptime(end, "%d/%m/%Y")
            else:
                end_dt = None

            try:
                result = parse(text)
                self.assertEqual(result[0], start_dt,
                                 "Error with string %s.\nGot %s, should be %s" % (
                    text, result[0], start_dt))
                self.assertEqual(result[1], end_dt,
                                 "Error with string %s.\nGot %s, should be %s" % (
                    text, result[1], end_dt))
            except ParseException:
                self.fail("Error with string %s.\nparse raised ParseException" % (text))


class TestFailingParsings(unittest.TestCase):
    tests = [
        # Various
        "27th Blah",
        "abfgsfgetgrw",
        "534th Jan 2010",
        "10th Aug 12345",
        "Turs 13th May 1998",
        "18 Octobre 2004",
        "to",
        "00000",
        "5 to",
        "Sept 12 to",
        "june november",
    ]

    def test(self):
        for test in self.tests:
            self.assertRaises(ParseException, parse, test)


class TestImplicitDaysParsings(unittest.TestCase):
    tests = [
        "May",
        "June to November",
        "2015",
        "2015 until 2016",
    ]

    def runTest(self):
        for test in self.tests:
            self.assertRaises(ParseException, parse, test, allow_implicit=False)
            parse(test, allow_implicit=True)
