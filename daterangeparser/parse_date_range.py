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

import datetime
import calendar

from pyparsing import ParseException, Optional, Word, oneOf, nums, stringEnd, Literal

MONTHS = {
    'jan': 1,
    'january': 1,
    'feb': 2,
    'february': 2,
    'mar': 3,
    'march': 3,
    'apr': 4,
    'april': 4,
    'may': 5,
    'jun': 6,
    'june': 6,
    'jul': 7,
    'july': 7,
    'aug': 8,
    'august': 8,
    'sep': 9,
    'sept': 9,
    'september': 9,
    'oct': 10,
    'october': 10,
    'nov': 11,
    'november': 11,
    'dec': 12,
    'december': 12
}


def check_day(tokens=None):
    """
    Converts to int and checks a day number, ensuring it is > 1 and < 31.
    """
    if not tokens:
        raise ParseException("Couldn't parse resulting datetime")

    t = int(tokens[0])
    if 1 <= t <= 31:
        return t
    else:
        raise ParseException("Couldn't parse resulting datetime")


def month_to_number(tokens):
    """
    Converts a given month in string format to the equivalent month number.

    Works with strings in any case, both abbreviated (Jan) and full (January).
    """
    month_name = tokens[0].lower()
    return MONTHS[month_name]


def post_process(res, allow_implicit=True):
    """
    Perform post-processing on the results of the date range parsing.

    At the moment this consists mainly of ensuring that any missing information is filled in.
    For example, if no years are specified at all in the string then both years are set to the
    current year, and if one part of the string includes no month or year then these are
    filled in from the other part of the string.

    :param res: The results from the parsing operation, as returned by the parseString function
    :param allow_implicit: If implicit dates are allowed
    :return: the results with populated date information
    """

    # Get current date
    today = datetime.date.today()

    if not allow_implicit:
        if ('start' in res and 'day' not in res.start) or ('end' in res and 'day' not in res.end):
            raise ParseException("Couldn't parse resulting datetime")

    if 'start' not in res:
        # We have a single date, not a range
        res['start'] = {}

        if 'month' not in res.end and 'day' not in res.end:
            # We have only got a year, so go from start to end of the year
            res['start']['year'] = res.end.year
            res['start']['month'] = 1
            res['start']['day'] = 1

            res['end']['month'] = 12
            res['end']['day'] = 31
            return res
        elif 'month' in res.end and 'day' not in res.end:

            if not isinstance(res.end.month, int):
                raise ParseException("Couldn't parse resulting datetime")

            # special case - treat bare month as a range from start to end of month
            if 'year' not in res.end or res.end.year == "":
                res['start']['year'] = today.year
                res['end']['year'] = today.year
            else:
                res['start']['year'] = res.end.year

            res['start']['day'] = 1
            res['start']['month'] = res.end.month

            res['end']['day'] = calendar.monthrange(
                res['start']['year'], res.end.month)[1]
        else:
            res['start']['day'] = res.end.day
            res['start']['month'] = res.end.month

            if 'year' not in res.end:
                res['start']['year'] = today.year
            else:
                res['start']['year'] = res.end.year

            res['end'] = None

        return res

    if 'month' not in res.end and 'month' not in res.start and \
            'day' not in res.end and 'day' not in res.start:
        # No months or days given, just years
        res['start']['month'] = 1
        res['start']['day'] = 1

        res['end']['month'] = 12
        res['end']['day'] = 31
        return res

    # Sort out years
    if 'year' not in res.end:
        res.end['year'] = today.year
        res.start['year'] = today.year
    elif 'year' not in res.start:
        res.start['year'] = res.end.year

    # Sort out months
    if 'month' not in res.start:
        res.start['month'] = res.end.month

    if 'day' not in res.start or res.start['day'] == '':
        res.start['day'] = 1

    if res.end.month and ('day' not in res.end or res.end['day'] == ''):

        res.end['day'] = calendar.monthrange(res.end.year, res.end.month)[1]

    return res


def create_parser():
    """Creates the parser using PyParsing functions."""

    # Day details (day number, superscript and day name)
    daynum = Word(nums, max=2)
    superscript = oneOf("th rd st nd", caseless=True)
    day = oneOf("Mon Monday Tue Tues Tuesday Wed Weds Wednesday "
                "Thu Thur Thurs Thursday Fri Friday Sat Saturday Sun Sunday", caseless=True)

    full_day_string = daynum + Optional(superscript).suppress()
    full_day_string.setParseAction(check_day)
    full_day_string.leaveWhitespace()

    # Month names, with abbreviations, with action to convert to equivalent month number
    month = oneOf(list(MONTHS.keys()), caseless=True) + \
        Optional(Literal(".").suppress())
    month.setParseAction(month_to_number)

    # Year
    year = Word(nums, exact=4)
    year.setParseAction(lambda tokens: int(tokens[0]))

    time_sep = oneOf(": .")
    am_pm = oneOf("am pm", caseless=True)
    hours = Word(nums, max=2)
    mins = Word(nums, max=2)

    time = hours("hour") + time_sep.suppress() + \
        mins("mins") + Optional(am_pm)("meridian")

    # date pattern
    date = (
        Optional(time).suppress() & Optional(full_day_string("day")) & Optional(day).suppress() &
        Optional(month("month")) & Optional(year("year"))
    )

    # Possible separators
    separator = oneOf("- -- to until through till untill \u2013 \u2014 ->", caseless=True)

    # Strings to completely ignore (whitespace ignored by default)
    ignoreable_chars = oneOf(", from starting beginning of", caseless=True)

    # Final putting together of everything
    daterange = (
        Optional(date("start") + Optional(time).suppress() + separator.suppress()) +
        date("end") + Optional(time).suppress() + stringEnd()
    )
    daterange.ignore(ignoreable_chars)

    return daterange


def parse(text, allow_implicit=True):
    """
    Parses a date range string and returns the start and end as datetimes.

    **Accepted formats:**

    This parsing routine works with date ranges and single dates, and should
    work with a wide variety of human-style string formats, including:

    - 27th-29th June 2010
    - 30 May to 9th Aug
    - 3rd Jan 1980 - 2nd Jan 2013
    - Wed 23 Jan - Sat 16 February 2013
    - Tuesday 29 May -> Sat 2 June 2012
    - From 27th to 29th March 1999
    - 1--9 Jul
    - 14th July 1988
    - 23rd October 7:30pm
    - From 07:30 18th Nov to 17:00 24th Nov

    **Notes:**

    - If an error encountered while parsing the date range then a
    `pyparsing.ParseException` will be raised.
    - If no year is specified then the current year is used.
    - All day names are ignored, so there is no checking to see whether,
    for example, the 23rd Jan 2013 is actually a Wednesday.
    - All times are ignored, assuming they are placed either before or after
    each date, otherwise they will cause an error.
    - The separators that are allows as part of the date range are `to`,
    `until`, `-`, `--` and `->`, plus the unicode em and en dashes.
    - Other punctuation, such as commas, is ignored.

    :param text: The string to parse
    :param allow_implicit: If implicit dates are allowed. For example,
    string 'May' by default treated as range
           from May, 1st to May, 31th. Setting allow_implicit to False helps avoid it.
    :return: A tuple ``(start, end)`` where each element is a datetime object.
    If the string only defines a single date then the tuple is ``(date, None)``.
    All times in the datetime objects are set to 00:00 as this function only parses dates.
    """
    parser = create_parser()

    # print text
    result = parser.parseString(text)
    # print result.dump()
    # print "----------"
    res = post_process(result, allow_implicit)
    # print res.dump()

    # Create standard dd/mm/yyyy strings and then convert to Python datetime
    # objects

    if 'year' not in res.start:
        # in case only separator was given
        raise ParseException("Couldn't parse resulting datetime")

    try:
        start_str = "%(day)s/%(month)s/%(year)s" % res.start
        start_datetime = datetime.datetime.strptime(start_str, "%d/%m/%Y")
    except ValueError:
        raise ParseException("Couldn't parse resulting datetime")

    if res.end is None:
        return start_datetime, None
    elif not res.end:
        raise ParseException("Couldn't parse resulting datetime")
    else:
        try:
            if "month" not in res.end:
                res.end["month"] = res.start["month"]
            end_str = "%(day)s/%(month)s/%(year)s" % res.end
            end_datetime = datetime.datetime.strptime(end_str, "%d/%m/%Y")
        except ValueError:
            raise ParseException("Couldn't parse resulting datetime")

        if end_datetime < start_datetime:
            # end is before beginning!
            # This is probably caused by a date straddling the change of year
            # without the year being given
            # So, we assume that the start should be the previous year
            res.start['year'] = res.start['year'] - 1
            start_str = "%(day)s/%(month)s/%(year)s" % res.start
            start_datetime = datetime.datetime.strptime(start_str, "%d/%m/%Y")

        return start_datetime, end_datetime


def interactive_test():
    """Sets up an interactive loop for testing date strings."""
    while True:
        text = input("Enter a date range string (or 'quit'): ")
        if text.lower() == 'quit':
            break

        # Get the PyParsing parser
        daterange = create_parser()

        res = daterange.parseString(text)

        res = post_process(res)

        start_str = "%(day)s/%(month)s/%(year)s" % res.start
        end_str = "%(day)s/%(month)s/%(year)s" % res.end

        start_datetime = datetime.datetime.strptime(start_str, "%d/%m/%Y")
        end_datetime = datetime.datetime.strptime(end_str, "%d/%m/%Y")

        print(text)
        print("From: %s" % start_str)
        print("To: %s" % end_str)
        print(start_datetime)
        print(end_datetime)
    print("----")
    # print res.dump()
