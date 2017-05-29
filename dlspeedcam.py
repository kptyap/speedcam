# Use Python 2.7
# This script to run once per week the day that the PDFs are updated
# 1. Download latest PDF on the WA Police website [x]
# 2. Convert PDF into CSV [x]

import tabula
import urllib
import os
import datetime

# set start date as the closest Monday prior, enddate as friday
d = datetime.datetime.today().weekday()
sd1 = datetime.date.today() - datetime.timedelta(days=d)
ed1 = sd1 + datetime.timedelta(days=6)
startdate1 = sd1.strftime('%d%m%Y')
enddate1 = ed1.strftime('%d%m%Y')

# Manually set the date here:
#startdate1 = '24042017'
#enddate1 = '30042017'

url = 'https://www.police.wa.gov.au/~/media/Files/Police/Traffic/Cameras/Camera-locations/MediaLocations-'+startdate1+'-to-'+enddate1+'.pdf'


#urllib.urlretrieve(url[, filename[, reporthook[, data]]])
urllib.urlretrieve(url, 'speedcamDL.pdf')

#check if pdf downloaded by checking file size
filesize = os.path.getsize('speedcamDL.pdf')

#if pdf was downloaded correctly then convert info to csv
if (filesize > 25000):
    tabula.convert_into("speedcamDL.pdf",
                            "speedcam.csv",
                            pages="all",
                            output_format="csv")
