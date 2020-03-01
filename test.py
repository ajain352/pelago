import dateutil.parser

s = "2015-08-16 23:05:52 UTC"
yourdate = dateutil.parser.parse(s)
print(yourdate)
