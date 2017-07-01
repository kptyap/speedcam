import csv
import psycopg2
import sys
import tabula
import urllib
import os
import tempfile
from datetime import datetime

#if pdf was downloaded correctly then convert info to csv
#check if pdf downloaded by checking file size

try:
    conn = psycopg2.connect("dbname=speedcams user=ubuntu host=localhost password=Kypw123!")
except:
    print('Cannot connect to db')

cur = conn.cursor()

# check if this pdf is new
cur.execute("SELECT DATE(got_date) FROM speedcamraw LIMIT 1;")
existing_date = cur.fetchone()
existing_date = existing_date[0]
print existing_date

csvfile = os.path.join(os.path.curdir, 'speedcam.csv')
print csvfile
with open (csvfile, 'rb') as csvfile:
    rows = list(csv.reader(csvfile, delimiter=','))
    new_date = (rows[0][0]).split(' ')
    new_date = new_date[3] +' '+ new_date[2] + ' '+ new_date[1]
    new_date = datetime.strptime(new_date, '%Y %B %d').date()
    print new_date

if (new_date == existing_date):
    print 'PDF has already been loaded'
    sys.exit()
else:
    print 'success, go run'

        