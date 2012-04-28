import unittest
import datetime
from parse_date_range import parse

class WorkingParsingTest(unittest.TestCase):
  tests = [ ("27th-29th June 2010", "27/06/2010",   "29/06/2010"),
            ("30 May - 9th Aug",    "30/05/XXXX",   "9/8/XXXX"),
            ("3rd Jan 1980 - 2nd Jan 2013", "3/1/1980", "2/1/2013"),
            ("Wed 23 Jan - Sat 16 February 2013", "23/1/2013", "16/2/2013"),
            ("Tue 29 May - Sat 2 June 2012", "29/5/2012", "2/6/2012"),
            ("1-9 Jul", "1/7/XXXX", "9/7/XXXX")  
  ]
  
  def runTest(self):
    for test in self.tests:
      text, start, end = test
      current_year = datetime.date.today().year
      start = start.replace("XXXX", str(current_year))
      end = end.replace("XXXX", str(current_year))
      start_dt = datetime.datetime.strptime(start, "%d/%m/%Y")
      end_dt = datetime.datetime.strptime(end, "%d/%m/%Y")
      
      result = parse(text)
      
      assert result[0] == start_dt, "%s not equal to %s" % (result[0], start_dt)
      assert result[1] == end_dt, "%s not equal to %s" % (result[1], end_dt)