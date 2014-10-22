import os
import unittest
import datetime

#configure our app to use the testing configuration
# --by setting the CONFIG_PATH environmental variable to point to a TestingConfig class(class created in config.py)
os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

import blog
from blog.filters import *

#class to hold our tests
class FilterTests(unittest.TestCase):
	#add couple of tests to make sure the dateformat function is working properly
	def testDateFormat(self):
		#tonight we're gonna party...
		date = datetime.date(1999, 12, 31)
		formatted = dateformat(date, "%y/%m/%d")
		self.assertEqual(formatted, "99/12/31")

	def testDateFormatNone(self):
		formatted = dateformat(None, "%y/%m/%d")
		self.assertEqual(formatted, None)

if __name__ == "__main__":
	unittest.main()