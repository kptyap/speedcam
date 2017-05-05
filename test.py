import datetime

# set start date as the closest Monday prior, enddate as friday
d = datetime.datetime.today().weekday()

sd1 = datetime.date.today() - datetime.timedelta(days=d)
ed1 = sd1 + datetime.timedelta(days=6)
startdate1 = sd1.strftime('%d%m%Y')
enddate1 = ed1.strftime('%d%m%Y')

print (sd1, ed1, startdate1, enddate1)




