import unittest
import datetime
from parse_date_range import parse

class WorkingParsingTest(unittest.TestCase):
  tests = [ 
            # Various 
            ("27th-29th June 2010", "27/06/2010",   "29/06/2010"),
            ("30 May - 9th Aug",    "30/05/XXXX",   "9/8/XXXX"),
            ("3rd Jan 1980 - 2nd Jan 2013", "3/1/1980", "2/1/2013"),
            ("Wed 23 Jan - Sat 16 February 2013", "23/1/2013", "16/2/2013"),
            ("Tuesday 29 May - Sat 2 June 2012", "29/5/2012", "2/6/2012"),
            ("1-9 Jul", "1/7/XXXX", "9/7/XXXX"),
            ("Tuesday 19th June - Wednesday 20th June 2013", "19/6/2013", "20/6/2013"),
            
            # Different separators
            ("14--16th May", "14/5/XXXX", "16/5/XXXX"),
            ("14-16th May", "14/5/XXXX", "16/5/XXXX"),
            ("14 - 16th May", "14/5/XXXX", "16/5/XXXX"),
            ("14 -- 16th May", "14/5/XXXX", "16/5/XXXX"),
            ("14--16th May", "14/5/XXXX", "16/5/XXXX"),
            ("14 to 16th May", "14/5/XXXX", "16/5/XXXX"),
            ("14 until 16th May", "14/5/XXXX", "16/5/XXXX"),
            (u"14 \u2013 16th May", "14/5/XXXX", "16/5/XXXX"),
            (u"14 \u2014 16th May", "14/5/XXXX", "16/5/XXXX"),
            (u"14-> 16th May", "14/5/XXXX", "16/5/XXXX"),
            
            # Individual Dates
            ("14th July 1988", "14/7/1988", None),
            ("1 May 2000", "1/5/2000", None),
            ("7 June", "7/6/XXXX", None),
            ("Saturday 19th July 1935", "19/7/1935", None)
            ("Sat 6 Aug", "6/8/XXXX", None)
  ]
  
  def runTest(self):
    for test in self.tests:
      text, start, end = test
      current_year = datetime.date.today().year
      start = start.replace("XXXX", str(current_year))
      start_dt = datetime.datetime.strptime(start, "%d/%m/%Y")

      if not end == None:
        end = end.replace("XXXX", str(current_year))
        end_dt = datetime.datetime.strptime(end, "%d/%m/%Y")
      else:
        end_dt = None
      
      result = parse(text)
      
      assert result[0] == start_dt, "Error with string %s. %s not equal to %s" % (text, result[0], start_dt)
      assert result[1] == end_dt, "Error with string %s. %s not equal to %s" % (text, result[1], end_dt)