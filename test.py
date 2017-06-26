import csv
import psycopg2
import sys
import tabula
import urllib
import os
import tempfile
from datetime import datetime

# Manually set the date here:
startdate1 = '12062017'
enddate1 = '18062017'

url = 'https://www.police.wa.gov.au/~/media/Files/Police/Traffic/Cameras/Camera-locations/MediaLocations-'+startdate1+'-to-'+enddate1+'.pdf'

#urllib.urlretrieve(url[, filename[, reporthook[, data]]])
urllib.urlretrieve(url, 'speedcamDL.pdf')

#check if pdf downloaded by checking file size
filesize = os.path.getsize('speedcamDL.pdf')
print filesize

#if pdf was downloaded correctly then convert info to csv
if (filesize > 30000):
    tabula.convert_into('speedcamDL.pdf',
                            'speedcam.csv',
                            pages='all',
                            output_format='csv')
else:
    print ('404 error')
    sys.exit



try:
    conn = psycopg2.connect("dbname=speedcams user=ubuntu host=localhost password=Kypw123!")
except:
    print('Cannot connect to db')

cur = conn.cursor()

# check if this pdf is new
cur.execute("SELECT DATE(got_date) FROM speedcamraw LIMIT 1;")
existing_date = cur.fetchone()
existing_date = existing_date[0]
#print existing_date

csvfile = '/home/ubuntu/workspace/speedcam/KY.csv'
with open (csvfile, 'rb') as csvfile:
    rows = list(csv.reader(csvfile, delimiter=','))
    new_date = (rows[0][0]).split(' ')
    new_date = new_date[3] +' '+ new_date[2] + ' '+ new_date[1]
    new_date = datetime.strptime(new_date, '%Y %B %d').date()
#    print new_date

if (new_date == existing_date):
    print 'PDF has already been loaded'
    sys.exit()
else:
    print 'success, go run'

        