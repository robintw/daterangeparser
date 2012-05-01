from pyparsing import *
import datetime

def check_day(tokens):
  """Converts to int and checks a day number, ensuring it is > 1 and < 31.
  
  """
  
  t = int(tokens[0])
  if t >= 1 and t <= 31:
    return t
  else:
    raise ParseException()
    
def month_to_number(tokens):
  """Converts a given month in string format to the equivalent month number.
  
  Works with strings in any case, both abbreviated (Jan) and full (January).
  
  """
  
  conversions = { 'jan' : 1,
                  'january' : 1,
                  'feb' : 2,
                  'february' : 2,
                  'mar' : 3,
                  'march' : 3,
                  'apr' : 4,
                  'april' : 4,
                  'may' : 5,
                  'jun' : 6,
                  'june': 6,
                  'jul' : 7,
                  'july' : 7,
                  'aug' : 8,
                  'august' : 8,
                  'sep' : 9,
                  'september' : 9,
                  'oct' : 10,
                  'october' : 10,
                  'nov' : 11,
                  'november' : 11,
                  'dec' : 12,
                  'december' : 12}
                  
  month_name = tokens[0].lower()
  return conversions[month_name]

def post_process(res):
  """Perform post-processing on the results of the date range parsing.
  
  At the moment this consists mainly of ensuring that any missing information is filled in.
  For example, if no years are specified at all in the string then both years are set to the
  current year, and if one part of the string includes no month or year then these are
  filled in from the other part of the string.
  
  Arguments:
  
  - ``res`` - The results from the parsing operation, as returned by the parseString function
  
  """

  # Get current date
  today = datetime.date.today()
  
  if 'start' not in res:
    # We have a single date, not a range
    res['start'] = {}
    res['start']['day'] = res.end.day
    res['start']['month'] = res.end.month
    if 'year' not in res.end:
      res['start']['year'] = today.year
    else:
      res['start']['year'] = res.end.year
    
    res['end'] = None
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
  
  return res

def create_parser():
  """Creates the parser using PyParsing functions."""
  
  # Day details (day number, superscript and day name)
  daynum = Word(nums, max=2)
  superscript = oneOf("th rd st nd", caseless=True)
  day = oneOf("Mon Monday Tue Tues Tuesday Wed Weds Wednesday Thu Thur Thurs Thursday Fri Friday Sat Saturday Sun Sunday", caseless=True)
  
  full_day_string = daynum + Optional(superscript).suppress()
  full_day_string.setParseAction(check_day)
  
  # Month names, with abbreviations, with action to convert to equivalent month number
  month = oneOf("Jan January Feb February Mar March Apr April May Jun June Jul July Aug August Sep September Oct October Nov November Dec December", caseless=True)
  month.setParseAction(month_to_number)
  
  # Year
  year = Word(nums, exact=4)
  year.setParseAction(lambda tokens: int(tokens[0]))
  
  time_sep = oneOf(": .")
  am_pm = oneOf("am pm", caseless=True)
  hours = Word(nums, max=2)
  mins = Word(nums, max=2)
  
  time = hours("hour") + time_sep.suppress() + mins("mins") + Optional(am_pm)("meridian")
  
  # Starting date
  first_date = Group(Optional(time).suppress() & Optional(day).suppress() & full_day_string("day") & Optional(month("month")) & Optional(year("year")))
  
  # Ending date
  last_date = Group(Optional(time).suppress() & Optional(day).suppress() & full_day_string("day") & month("month") & Optional(year("year")))
  
  # Possible separators
  separator = oneOf(u"- -- to until \u2013 \u2014 ->", caseless=True)
  
  # Strings to completely ignore (whitespace ignored by default)
  ignoreable_chars = oneOf(", from", caseless=True)
  
  # Final putting together of everything
  daterange = Optional(first_date("start") + separator.suppress()) + last_date("end") + stringEnd
  daterange.ignore(ignoreable_chars)

  return daterange

def parse(text):
  """Parses a date range string and returns the start and end as datetimes. 
  
  **Arguments:**
  
  - ``text`` - The string to parse
  
  **Returns:**
  
  A tuple ``(start, end)`` where each element is a datetime object. If the string only defines a single
  date then the tuple is ``(date, None)``. All times in the datetime objects are set to 00:00 as
  this function only parses dates.
  
  **Accepted formats:**
  
  This parsing routine works with date ranges and single dates, and should work with a wide variety of
  human-style string formats, including:
  
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
  
  - If an error encountered while parsing the date range then a `pyparsing.ParseException` will be raised.
  - If no year is specified then the current year is used.
  - All day names are ignored, so there is no checking to see whether, for example, the 23rd Jan 2013 is actually a Wednesday.
  - All times are ignored, assuming they are placed either before or after each date, otherwise they will cause an error.
  - The separators that are allows as part of the date range are `to`, `until`, `-`, `--` and `->`, plus the unicode em and en dashes.
  - Other punctuation, such as commas, is ignored.
  
  """
  parser = create_parser()
  
  result = parser.parseString(text)
  #print result.dump()
  #print "----------"
  res = post_process(result)
  #print res.dump()
  
  # Create standard dd/mm/yyyy strings and then convert to Python datetime objects
  start_str = "%(day)s/%(month)s/%(year)s" % res.start
  start_datetime = datetime.datetime.strptime(start_str, "%d/%m/%Y")
  
  if res.end == None:
    return (start_datetime, None)
  else:
    end_str = "%(day)s/%(month)s/%(year)s" % res.end
    end_datetime = datetime.datetime.strptime(end_str, "%d/%m/%Y")
  
    return (start_datetime, end_datetime)
  
def interactive_test():
  """Sets up an interactive loop for testing date strings."""
  while True:
    text = raw_input("Enter a date range string (or 'quit'): ")
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
    
    print text
    print "From: %s" % start_str
    print "To: %s" % end_str
    print start_datetime
    print end_datetime
  print "----"
  #print res.dump()